import re
from collections import Counter


def words(text):
    return re.findall(r'\w+', text.lower())


dictionary = Counter(words(open('indexing/big.txt', 'r').read()))


def P(word, N=sum(dictionary.values())):
    return dictionary[word] / N


def clac_edit_distance(str1, str2):
    m = len(str1)
    n = len(str2)
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j

            elif j == 0:
                dp[i][j] = i

            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]

            else:
                dp[i][j] = 1 + min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1])

    return dp[m][n], m


def main():
    query = input()
    candidates = dict()
    for wrd in dictionary:
        dist, wl = clac_edit_distance(query, wrd)
        if dist == 0:
            print(query + " is a correct word")
            return
        if dist == 1:
            candidates[wrd] = ((wl - dist) / wl) * 10000
        if dist == 2:
            candidates[wrd] = ((wl-dist) / wl)

    if not candidates:
        print('No spelling correction found')
        return

    mpw = list(filter(lambda x: x[1] != 1,  candidates.items()))
    mpw = list(map(lambda x: (x[0], P(x[0])*x[1]),  mpw))
    mpw = sorted(mpw, key=lambda x: -x[1])
    print(mpw[0][0], ' is the most probable correct spelling')


if __name__ == "__main__":
    main()
