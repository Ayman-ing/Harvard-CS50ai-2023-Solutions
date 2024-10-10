import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }


    # Loop over all sets of people who might have the trait
    names = set(people)



    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    def get_gene_number(person, one_gene, two_genes):
        if person in one_gene:
            return 1
        elif person in two_genes:
            return 2
        else:
            return 0
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    def base_gene_probability(person, one_gene, two_genes, have_trait):
        if person not in one_gene and person not in two_genes:
            return PROBS["gene"][0] * PROBS["trait"][0][person in have_trait]
        elif person in one_gene:
            return PROBS["gene"][1] * PROBS["trait"][1][person in have_trait]
        else:
            return PROBS["gene"][2] * PROBS["trait"][2][person in have_trait]
   
    def parent_inherit_gene_probability(person, one_gene, two_genes, have_trait):
        def no_gene_from_parent(parent_gene_number):
            if parent_gene_number==2:
                return 0.01
            elif  parent_gene_number==1:
                return 0.5
            else :
                return 0.99
        def gene_from_parent(parent_gene_number):
            if parent_gene_number ==2:
                return 0.99
            elif  parent_gene_number ==1:
                return 0.5
            else :
                return 0.01

        father_gene_number= get_gene_number(people[person]["father"], one_gene, two_genes)
        mother_gene_number= get_gene_number(people[person]["mother"], one_gene, two_genes)
        person_gene_number= get_gene_number(person, one_gene, two_genes)
        prob =1
        if person_gene_number==0:
           prob= no_gene_from_parent(mother_gene_number)*no_gene_from_parent(father_gene_number)
        elif person_gene_number==1:
            prob= gene_from_parent(mother_gene_number)*no_gene_from_parent(father_gene_number) + gene_from_parent(father_gene_number)*no_gene_from_parent(mother_gene_number)
        else:
            prob= gene_from_parent(mother_gene_number)*gene_from_parent(father_gene_number)
        return prob*PROBS["trait"][person_gene_number][person in have_trait]

    proba = 1
    for p in people.keys() :
        if people[p]["mother"] is None and  people[p]["father"] is None:
            proba*=base_gene_probability(p, one_gene, two_genes, have_trait)
    for p in people.keys() :
        if people[p]["mother"] is None  or  people[p]["father"] is None :
            continue 
        proba*=parent_inherit_gene_probability(p, one_gene, two_genes, have_trait)
    return proba



                 


            

    


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities.keys():
        if person in two_genes:
            probabilities[person]["gene"][2]+=p
        elif person in one_gene:
             probabilities[person]["gene"][1]+=p
        else:
            probabilities[person]["gene"][0]+=p
        if person in have_trait:
            probabilities[person]["trait"][True]+=p
        else:
            probabilities[person]["trait"][False]+=p
            



def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities.keys():
        gene_distribution_sum =sum(probabilities[person]["gene"].values())
        trait_distribution_sum =sum(probabilities[person]["trait"].values())
        for gene in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene] /= gene_distribution_sum
    
        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] /= trait_distribution_sum

if __name__ == "__main__":
    main()