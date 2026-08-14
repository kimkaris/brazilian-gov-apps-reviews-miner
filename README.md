# Brazilian Government Apps Reviews Miner
This repository contains the extraction and data processing scripts developed for my master's dissertation. 
The goal of this pipeline is to mine user reviews on the Google Play Store to identify flaws, privacy complaints, and risk perceptions regarding the use of massively adopted Brazilian government platforms: **gov.br**, **Meu INSS**, and **CNH do Brasil**.

The extraction and analysis workflow was built to ensure methodological reproducibility, being executed in two steps:
1. **`collect_reviews.py`:** Responsible for scraping data directly from the app store. The script extracts reviews based on a maximum star rating limit defined by the user (e.g., 1 to 4 stars) and natively exports the results to a `.csv` format.
2. **`review_filter_and_classify.py`:** Processes the raw file generated in the previous step using vectorized operations. The script cross-references the texts with a predefined list of keywords (`PRIVACY_LIST`) and applies 8 thematic category tags, generating the final dataset ready for qualitative analysis.

## How to Run
(These scripts were developed and validated only in a Linux environment. Python and the utilized libraries are cross-platform. If you encounter any unexpected behavior, please contact me)

1. Make sure you have Python installed. I highly recommend that you create and activate a virtual environment. Then, install the required dependencies:
```bash
pip install google-play-scraper pandas
```
2. Run the collection script depending on your O.S.:
- Linux/MacOs
```bash
  python3 collect_reviews.py
```
- Windows
```bash
  python collect_reviews.py
```

The terminal will prompt for the maximum rating allowed for extraction. The result will be saved in partitioned files (such as `app_reviews_part_1.csv`)

3. Ensure the generated .csv file is in the same directory and run the filtering script:
- Linux/MacOs
```bash
  python3 review_filter_and_classify.py
```
- Windows
```bash
  python review_filter_and_classify.py
```

The final filtered database containing the assigned category columns, will be saved as `categorized_reviews.csv`
  
## References

The keyword dictionaries (`PRIVACY_LIST` and `CATEGORIES`) used in the filtering step of this project were adapted and translated to portuguese (PT-BR) from the methodology proposed by **Haggag et al. (2025)**.
If you use or build upon the filtering logic, consider citing the original authors:
* HAGGAG, O.; PEDACE, A.; PAN, S.; GRUNDY, J. An analysis of privacy regulations and user concerns of finance mobile applications. *Information and Software Technology*, v. 184, p. 107756, 2025.
* [Repository](https://github.com/HumaniSELab/An_Analysis_of_Privacy_Regulations_and_User_Concerns_of_Finance_Mobile_Applications)
