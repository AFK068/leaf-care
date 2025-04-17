# About 

Telegram bot that allows you to identify diseases of a certain list of plants by a photo of a leaf.

<p align="center">
    <img src="./assets/use.gif" alt="Demo">
</p>

# Architecture

![Architecture](./assets/architecture.png)

# 🌿 Disease Detection Pipeline

When a user sends an image of a potentially diseased plant, the following process is initiated:

1. **Leaf Detection (YOLOv11):**  
   The system first applies a YOLO-based leaf detection model ([YOLO](https://docs.ultralytics.com/ru/models/yolo11/)) to identify plant leaves in the image.

   <p align="center">
       <img src="assets/detect.jpg" alt="Bacterial spot" width="500">
   </p>

2. **Leaf Cropping:**  
   If at least one leaf is detected, each detected leaf is cropped from the image. A list of cropped leaf images is generated for further analysis.

3. **Load Balancing and Classification (gRPC + NGINX):**  
   The cropped leaf images are sent via **gRPC** to an **NGINX** load balancer, which distributes the processing load across multiple identical classification servers running in parallel. This ensures scalability and speeds up inference time.

4. **Disease Classification:**  
   Each cropped leaf image is processed by machine learning models trained for **multi-class classification** of diseases. The classification results for all leaves are aggregated and sent back to the client (i.e., the bot).

5. **Result Aggregation and Decision Making (Bot):**  
   The bot aggregates probabilities across all detected leaves. If the probability that the plant is **healthy** is high enough, the bot informs the user but still provides the **top 3 most probable diagnoses** as a precaution.

   If the plant is likely **diseased**, the bot explicitly informs the user and provides the top 3 most probable diseases. For each suggested disease, it includes:
   - 📖 Name of the disease
   - 📷 An example image of the disease for comparison
   - 🔗 A link to a detailed article explaining the disease


# Classes
## 🍅 Tomato

### [Bacterial spot](https://hort.extension.wisc.edu/articles/bacterial-spot-of-tomato/)
<p align="center">
    <img src="https://hort.extension.wisc.edu/files/2017/03/Bacterial-spot-on-tomato-leaves-e1721249493890.jpg" alt="Bacterial spot" width="300">
</p>

---

### [Early blight](https://www.missouribotanicalgarden.org/gardens-gardening/your-garden/help-for-the-home-gardener/advice-tips-resources/insects-pests-and-problems/diseases/fungal-spots/early-blight-of-tomato)
<p align="center">
    <img src="https://www.missouribotanicalgarden.org/Portals/0/Gardening/Gardening%20Help/images/Pests/Pest2369.jpg" alt="Early blight" width="300">
</p>

---

### [Late blight](https://vegpath.plantpath.wisc.edu/diseases/tomato-late-blight/)
<p align="center">
    <img src="https://content.peat-cloud.com/w400/tomato-late-blight-tomato-1556463954.jpg" alt="Late blight" width="300">
</p>

---

### [Leaf mold](https://extension.umn.edu/disease-management/tomato-leaf-mold)
<p align="center">
    <img src="https://extension.umn.edu/sites/extension.umn.edu/files/tomato-leaf-mold.jpg" alt="Leaf mold" width="300">
</p>

---

### [Septoria leaf spot](https://www.missouribotanicalgarden.org/gardens-gardening/your-garden/help-for-the-home-gardener/advice-tips-resources/insects-pests-and-problems/diseases/fungal-spots/septoria-leaf-spot-of-tomato)
<p align="center">
    <img src="https://www.missouribotanicalgarden.org/Portals/0/Gardening/Gardening%20Help/images/Pests/Septoria_Leaf_Spot_of_Tomato186.jpg" alt="Septoria leaf spot" width="300">
</p>

---

### [Two-spotted spider mite](https://entomology.ca.uky.edu/ef310)
<p align="center">
    <img src="https://entomology.ca.uky.edu/files/inline-images/310a.jpg?itok=1J_F2GXG" alt="Two-spotted spider mite" width="300">
</p>

---

### [Target spot](https://www.vegetables.bayer.com/ca/en-ca/resources/agronomic-spotlights/target-spot-of-tomato.html)
<p align="center">
    <img src="https://apps.lucidcentral.org/pppw_v10/images/entities/tomato_target_spot_163/img_4795.jpg" alt="Target spot" width="300">
</p>

---

### [Yellow leaf curl virus](https://agriculture.vic.gov.au/biosecurity/plant-diseases/vegetable-diseases/tomato-yellow-leaf-curl-virus)
<p align="center">
    <img src="https://source.roboflow.com/i0iadecycQWNql6Gvk8vUECFpZH3/m4AKB7sZ5GcnjStMWJgA/thumb.jpg" alt="Yellow leaf curl virus" width="300">
</p>

---

### [Mosaic virus](https://en.wikipedia.org/wiki/Tomato_mosaic_virus)
<p align="center">
    <img src="https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcTXGHj1MECzKsiaMcrjVJT2BKGkKY0euFAmRdkGKhk6W9TS84qkKuO1yqCDtrDk0uCnPK3YV6KmTEOiMODbsXXt7gn7iN2RtxqdYIBXRg" alt="Mosaic virus" width="300">
</p>

## 🥒 Cucumber

### [Anthracnose](https://www.gardeningknowhow.com/edible/vegetables/cucumber/anthracnose-control-in-cucumbers.htm)
<p align="center">
    <img src="https://cdn.mos.cms.futurecdn.net/dYHfbiytbsKMxicbRhK4x3-768-80.jpg.webp" alt="Anthracnose" width="300">
</p>

---

### [Bacterial Wilt](https://www.missouribotanicalgarden.org/gardens-gardening/your-garden/help-for-the-home-gardener/advice-tips-resources/insects-pests-and-problems/diseases/bacterial-spots/bacterial-wilt-of-cucumber)
<p align="center">
    <img src="https://hort.extension.wisc.edu/files/2021/02/Bacterial_Wilt_of_Cucurbits.jpg" alt="Bacterial Wilt" width="300">
</p>

---

### [Downy Mildew](https://www.ontario.ca/page/downy-mildew-greenhouse-cucumber)
<p align="center">
    <img src="https://extension.umn.edu/sites/extension.umn.edu/files/cucumber-leaf-mildew.jpg" alt="Downy Mildew" width="300">
</p>

---

### [Gummy Stem Blight](https://www.ontario.ca/page/gummy-stem-blight-greenhouse-cucumber#:~:text=Gummy%20stem%20blight%20is%20a,is%20also%20called%20mycosphaerella%20rot.)
<p align="center">
    <img src="https://apps.lucidcentral.org/pppw_v10/images/entities/cucumber_gummy_stem_blight_201/diyleafgh.jpg" alt="Gummy Stem Blight" width="300">
</p>


## 🍈 Melon

### [Anthracnose](https://plantwiseplusknowledgebank.org/doi/10.1079/pwkb.20157800697#:~:text=Anthracnose%20damage%20on%20melon%20fruits,sunken%20with%20a%20yellowish%20colour.)
<p align="center">
    <img src="https://s3-us-west-1.amazonaws.com/sg-production-public/data/images/508/files/big_anthracnose.jpg" width="300">
</p>

---

### [Downy Mildew](https://extension.umn.edu/disease-management/downy-mildew-cucurbits)
<p align="center">
    <img src="https://lh3.googleusercontent.com/proxy/j_5PmjDpL4Gkd7NGIuJ-0RjteQb8BdZ3nW98BdgpXsKCQQklMRwgSCkPgjVn6XgeX5DgBGc0WlzJAWStbOiVtGkGBPDcypAxWyhFUAKDrXA_7xKXRJwyrI2arrmTnM0" alt="Downy Mildew" width="300">
</p>


## 🍉 Watermelon


### [Downy Mildew](https://www.vegetables.bayer.com/language-masters/en-us/resources/growing-tips-and-innovation-articles/agronomic-spotlights/watermelon-downy-mildew.html)
<p align="center">
    <img src="https://vegcropshotline.org/wp-content/uploads/2016/02/602-113-0.jpg" alt="Downy Mildew" width="300">
</p>

---

### [Mosaic Virus](https://en.wikipedia.org/wiki/Watermelon_mosaic_virus)
<p align="center">
    <img src="https://extension.usu.edu/planthealth/ipm/images/agricultural/vegetables/Watermelon-mosaic-virus-2apumpkin.jpg" alt="Mosaic Virus" width="300">
</p>

## 🍓 Strawberry


### [Calcium Deficiency](https://ucanr.edu/site/strawberry-disorders-identification-management/calcium-deficiency)
<p align="center">
    <img src="https://ucanr.edu/sites/default/files/styles/ex/public/2012-12/158006.jpg.webp?itok=A-zoJo2Z" alt="Calcium Deficiency" width="300">
</p>

---

### [Angular Leaf Spot](https://ohioline.osu.edu/factsheet/HYG-3212-11)
<p align="center">
    <img src="https://plant-pest-advisory.rutgers.edu/wp-content/uploads/2013/10/BLS-Leaf-300x199.jpg" alt="Angular Leaf Spot" width="300">
</p>

---

### [Leaf Spot](https://hort.extension.wisc.edu/articles/common-leaf-spot-of-strawberry/)
<p align="center">
    <img src="https://hort.extension.wisc.edu/files/2024/08/Common_Leaf_Spot_of_Strawberry.jpg" alt="Leaf Spot" width="300">
</p>

---

### [Powdery Mildew](https://blogs.cornell.edu/berrytool/strawberries/powdery-mildew/)
<p align="center">
    <img src="https://blogs.cornell.edu/berrytool/files/2017/01/strpm30-opt-2-1yl0vby.jpg" alt="Powdery Mildew" width="300">
</p>

## 🫑 Pepper


### [Bacterial Spot](https://extension.wvu.edu/lawn-gardening-pests/plant-disease/fruit-vegetable-diseases/bacterial-leaf-spot-of-pepper)
<p align="center">
    <img src="https://extension.wvu.edu/files/50d2bf3d-125f-4b45-9c03-487959bd8344/893x595?cb=0862b40bec913b574f1f05f79f2805c7" alt="Bacterial Spot" width="300">
</p>

---

### [Leaf Blight](https://www.pepperhub.in/what-is-leaf-blight/?srsltid=AfmBOoqZQQ5W2BkjVZgPebhF6cK_uZg9Mltvui2Ekc2yj6fQculZTH01)
<p align="center">
    <img src="https://upload.wikimedia.org/wikipedia/commons/9/90/Phytophthora_leaf_blight_of_taro_%28Colocasia_esculenta%29_%2814833256493%29.jpg" alt="Leaf Blight" width="300">
</p>

---

### [Yellow Mottle Virus](https://www.sciencedirect.com/science/article/abs/pii/S2452014422001881#:~:text=The%20piper%20yellow%20mottle%20virus,it%20causes%20the%20stunt%20disease.)
<p align="center">
    <img src="https://media.springernature.com/lw1200/springer-static/image/art%3A10.1007%2Fs13337-021-00686-3/MediaObjects/13337_2021_686_Fig1_HTML.jpg" alt="Yellow Mottle Virus" width="300">
</p>

# How to Use

1. **Download the models**  
    Download and unzip the archive from [Yandex Disk](https://disk.yandex.ru/d/6ip0_MoAuxq50w).

2. **Place the detection model**  
    Copy `leaf_detect.pt` into `bot/models/leaf_detect.pt`.

3. **Place the classification models**  
    Copy each file into `mlcore/models/` with the exact filename:
    - `cucumber_cls_model.pt` — Cucumber
    - `melons_cls_model.pt` — Melon
    - `pepper_cls_model.pt` — Pepper
    - `strawberrie_cls_model.pt` — Strawberry
    - `tomato_cls_model.pt` — Tomato
    - `watermelon_cls_model.pt` — Watermelon

4. **Prerequisites**  
    Ensure you have:
    - Docker Compose installed.
    - A valid Telegram Bot Token.

5. **Start the bot**  
    From the project root, run:
    ```bash
    BOT_TOKEN=<YOUR_TELEGRAM_BOT_TOKEN> docker-compose up -d
    ```