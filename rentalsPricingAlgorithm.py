import pandas as pd
import os
import logging
import logging.handlers
import datetime, time

csvDataFrame = pd.read_csv(r"C:\Users\Vijay Chellappan\Desktop\T\FullStackCodingChallenge\FullStackCodingChallenge\challenge_data.csv", usecols=['price_per_sqfoot','bedrooms','bathrooms'])
bedType = csvDataFrame.bedrooms.sort_values(ascending=True).unique()
bathType = csvDataFrame.bathrooms.sort_values(ascending=True).unique()

def get_logger(t_dir, s_time):

    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)

    # Set Logger Time
    logger_date = datetime.datetime.fromtimestamp(s_time).strftime('%Y_%m_%d')
    logger_time = datetime.datetime.fromtimestamp(s_time).strftime('%H_%M_%S')

    # Debug Handler for Console Checks - logger.debug(msg)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    log.addHandler(console_handler)

    # Ensure Logs Directory Exists
    l_dir = os.path.join(t_dir, 'logs', logger_date)
    if not os.path.exists(l_dir):
        os.makedirs(l_dir)

    # Log Handler for Reports - logger.info(msg)
    log_handler = logging.FileHandler(os.path.join(l_dir, 'User_Report_{}.txt'.format(logger_date)), 'w')
    log_handler.setLevel(logging.INFO)
    log.addHandler(log_handler)

    log.info('Script Started: {} - {}\n'.format(logger_date, logger_time))

    return log, l_dir

def calculateStats():
    
    try:
        dataframeCollection = {}
        meanStats = {}
        medianStats = {}
        for numberOfBeds in bedType:
            for numberOfBaths in bathType:
                #print(numberOfBeds,numberOfBaths)
                dataframeCollection[numberOfBeds,numberOfBaths] = csvDataFrame.loc[(csvDataFrame['bedrooms'] == numberOfBeds) & (csvDataFrame['bathrooms'] == numberOfBaths)]
                #meanStats[numberOfBeds,numberOfBaths] = dataframeCollection[numberOfBeds,numberOfBaths]["price_per_sqfoot"].mean()
                medianStats[numberOfBeds,numberOfBaths] = dataframeCollection[numberOfBeds,numberOfBaths]["price_per_sqfoot"].median()
        return meanStats,medianStats 
    
    except Exception as e:
        logger.exception(e)
     
        
def getOptimalPricing(numberOfBeds,numberOfBaths,totalSquareFootage):
    
    try:
        csvDataFrame = pd.read_csv(r"C:\Users\Vijay Chellappan\Desktop\T\FullStackCodingChallenge\FullStackCodingChallenge\challenge_data.csv", usecols=['price_per_sqfoot','bedrooms','bathrooms'])
        meanPrice_persqft = csvDataFrame.loc[(csvDataFrame['bedrooms'] == numberOfBeds) & (csvDataFrame['bathrooms'] == numberOfBaths)]["price_per_sqfoot"].mean()
        medianPrice_persqft = csvDataFrame.loc[(csvDataFrame['bedrooms'] == numberOfBeds) & (csvDataFrame['bathrooms'] == numberOfBaths)]["price_per_sqfoot"].median()
        meanPrice = meanPrice_persqft*totalSquareFootage
        medianPrice = medianPrice_persqft*totalSquareFootage
        return meanPrice, medianPrice
 
    except Exception as e:
        logger.exception(e)
        
if __name__ == "__main__":
    try:
        start_time = time.time()
        this_dir = os.path.split(os.path.realpath(__file__))[0]
        logger, log_dir = get_logger(this_dir, start_time)
        meanStats, medianStats = calculateStats()
        numberOfBeds = 2
        numberOfBaths = 2
        totalSquareFootage = 1250
        meanPrice, medianPrice = getOptimalPricing(numberOfBeds,numberOfBaths,totalSquareFootage)
        print( meanPrice, medianPrice)
    except Exception as e:
        logger.exception(e)