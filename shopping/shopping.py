import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    month_dict = {
        "Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "June": 5,
        "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11
    }
    with open(filename, 'r') as file:
            evidence=[]
            labels=[]
            reader = csv.DictReader(file)
            for row in reader:
                # Create list 'e' by adding values in the required order
                e = [
                    int(row["Administrative"]),
                    float(row["Administrative_Duration"]),
                    int(row["Informational"]),
                    float(row["Informational_Duration"]),
                    int(row["ProductRelated"]),
                    float(row["ProductRelated_Duration"]),
                    float(row["BounceRates"]),
                    float(row["ExitRates"]),
                    float(row["PageValues"]),
                    float(row["SpecialDay"]),
                    month_dict[row["Month"]],
                    int(row["OperatingSystems"]),
                    int(row["Browser"]),
                    int(row["Region"]),
                    int(row["TrafficType"]),
                    1 if row["VisitorType"] == "Returning_Visitor" else 0,
                    1 if row["Weekend"] == "TRUE" else 0
                ]     
                evidence.append(e)
                labels.append(1 if row["Revenue"] else 0)
    return evidence,labels
    

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence,labels)
    return model


def evaluate(labels, predictions):
    TrueCorrect =0
    TrueIncorrect=0
    totalTrue=0
    falseCorrect = 0
    falseIncorrect=0
    totalFalse=0
    for actual,predicted in zip(labels,predictions):
        if(actual==1):
            totalTrue+=1
            if actual==predicted:
                TrueCorrect +=1
            else:
                TrueIncorrect+=1
        else:
            totalFalse+=1
            if actual==predicted:
                falseCorrect +=1
            else:
                falseIncorrect+=1 
    print(totalFalse,totalTrue)
    positiveRate=0
    negativeRate=0
    if totalTrue!=0:
        positiveRate=TrueCorrect/totalTrue
    if totalFalse!=0:
        negativeRate =falseCorrect/totalFalse


    return positiveRate,negativeRate
         
    


if __name__ == "__main__":
    main()
