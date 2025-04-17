import json
from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import Optional

import aiofiles

from bot.logger import logger
from bot.protos.predict import predict_pb2


@dataclass
class DiseaseResult:
    class_name: str
    probability: float
    description: str = ""
    photo_url: str = ""
    reference_url: str = ""


class PlantDiagnostics:
    _instance: Optional["PlantDiagnostics"] = None
    _lock: Lock = Lock()
    _db: Optional[dict] = None

    def __new__(cls):
        logger.debug("Creating a new instance of PlantDiagnostics")

        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    async def _load_db(self):
        if self._db is not None:
            return self._db

        db_path = Path(__file__).parent.parent.parent / "data" / "diseases_db.json"
        async with aiofiles.open(db_path, encoding="utf-8") as f:
            self._db = json.loads(await f.read())

        logger.debug("Loaded diseases database")
        return self._db

    async def analyze_and_report(self, results: predict_pb2.PredictorReply, plant_type: str) -> str:
        db = await self._load_db()

        raw_results = []

        raw_results.extend(
            {
                "class_name": class_prob.class_name,
                "probability": class_prob.probability,
            }
            for image_result in results.result
            for class_prob in image_result.results
        )

        processed = await self._process_results(raw_results, plant_type, db)
        aggregated = await self._aggregate_results(processed)

        return await self._generate_report(aggregated)

    async def _process_results(
        self,
        results: list[dict],
        plant_type: str,
        db: dict,
    ) -> list[DiseaseResult]:
        plant_diseases = db.get(plant_type, {}).get("diseases", [])
        processed = []

        for result in results:
            class_name = result["class_name"]
            probability = result["probability"]

            info = next(
                (
                    disease
                    for disease in plant_diseases
                    if disease["class_name"].lower() == class_name.lower()
                ),
                None,
            )

            processed.append(DiseaseResult(
                class_name=class_name,
                probability=probability,
                description=info.get("description", ""),
                photo_url=info.get("photo_url", ""),
                reference_url=info.get("reference_url", ""),
            ))

        return processed

    async def _aggregate_results(self, results: list[DiseaseResult]) -> dict[str, DiseaseResult]:
        aggregated = {}

        for result in results:
            class_name = result.class_name
            if class_name not in aggregated:
                aggregated[class_name] = result
            else:
                aggregated[class_name].probability += result.probability

        total = sum(r.probability for r in aggregated.values())
        if total > 0:
            for result in aggregated.values():
                result.probability /= total

        return aggregated

    async def _generate_report(self, aggregated: dict[str, DiseaseResult]) -> list[str]:
        healthy_result = next(
            (
                result
                for class_name, result in aggregated.items()
                if "healthy" in class_name.lower()
            ),
            None,
        )

        is_healthy = healthy_result and healthy_result.probability > 0.9

        sorted_results = sorted(
            aggregated.values(),
            key=lambda x: x.probability,
            reverse=True,
        )

        report_lines = []

        if is_healthy:
            report_lines.append(
                f"🟢 Растение здорово - вероятность {healthy_result.probability:.1%}.\n\n"
                f"📌 Рекомендуем всё равно проверить состояние растения.",
            )
        else:
            report_lines.append("🔴 Растение может быть больным. Вот подробности:")

        messages = ["\n".join(report_lines)]

        top_diseases = [
            d for d in sorted_results if "healthy" not in d.class_name.lower()
        ][:min(3, len(sorted_results))]

        for disease in top_diseases:
            emoji = "🟡" if disease.probability < 0.5 else "🔴"
            disease_message = (
                f"{emoji} {disease.description} - вероятность {disease.probability:.1%}\n\n"
                f"Фото: {disease.photo_url}\n\n"
                f"Подробнее: {disease.reference_url}"
            )
            messages.append(disease_message)

        return messages
