from data.data_preprocess_1 import data_preprocess1
from data.data_preprocess_2 import data_preprocess2
from models.RecGFI import recgfi,recgfi_diffthres,recgfi_timesorted,recgfi_crosspro
from models.wordcloud import drawwordcloud
import logging
if __name__=="__main__":
    logging.basicConfig(
        format="%(asctime)s (Process %(process)d) [%(levelname)s] %(filename)s:%(lineno)d %(message)s",
        level=logging.INFO)
    logging.info("Start!")
    data_preprocess1()
    data_preprocess2()
    logging.info("Data is processed.")
    recgfi_diffthres()
    logging.info("Results under different thresholds are available at Different_threshold.csv.")
    recgfi_timesorted()
    logging.info("Results for time-sorted issues are available at Time_sorted_dataset.csv.")
    recgfi_crosspro()
    logging.info("Cross-projects results are available at Cross_projects_dataset.csv.")
    recgfi()
    logging.info("Comparision with baselines are available at Timepoint_1_threshold_0.csv and Timepoint_1_threshold_0.csv.")
    drawwordcloud()
    logging.info("Wordclouds of keywords are drawn.")
    logging.info("Finish!")
