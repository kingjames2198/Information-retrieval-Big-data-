from indexing import clean, indexer, preprocess

if __name__ == '__main__':
    # clean the dataset
    clean.clean_dataset()

    # pre-process the data i.e. do stemming and remove stop words etc.
    preprocess.pre_processing()

    # create the inverted index for the pre processed data
    indexer.create_index()
    word = input("Enter word to get the documents : ")
    indexer.search(word)
