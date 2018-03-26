
class MomentumStrategy(object):
    def segment_momentum_probability(days, change_pd):

        lists = []
        first_day = 900
        for i in range(len(change_pd.iloc[first_day:])-days):
            input = change_pd.iloc[i:i+days].tolist()
            bool_input = []
            for item in input:
                if item > 0:
                    bool_input.append(True)
                else: bool_input.append(False)
            result = change_pd.iloc[i+days]
            bool_result = True if result>0 else False
            bool_input.append(bool_result)
            lists.append(tuple(bool_input))

        hashmap = dict()
        for item in lists:
            if item in hashmap:
                hashmap[item] += 1
            else:
                hashmap[item] = 1

        new_list = []
        for key, value in hashmap.items():
            new_list.append(((key), value*100/len(lists)))

        print(new_list)


    def segment_momentum_probability2(day, df, segments):
        day_df = df.loc[df['Date'] == day]
        change = 100*(day_df['Close']-day_df['Open'])/day_df['Open']
        lists = []
        for i in range(len(change.iloc[0:])-segments):
            input = change.iloc[i:i+segments].tolist()
            bool_input = []
            for item in input:
                if item > 0:
                    bool_input.append(True)
                else: bool_input.append(False)
            result = change.iloc[i+segments]
            bool_result = True if result>0 else False
            # bool_input.append(bool_result)
            # lists.append(tuple(bool_input))
            input.append(result)
            clustered = cluster_list(input)
            lists.append(clustered)

        hashmap = dict()
        for item in lists:
            if item in hashmap:
                hashmap[item] += 1
            else:
                hashmap[item] = 1

        new_list = []
        for key, value in hashmap.items():
            new_list.append(((key), value*100/len(lists)))

        print(new_list)

    def cluster_list(input):
        ans = []
        for item in input:
            if item >= 1:
                ans.append('A')
            elif item >= .5:
                ans.append('B')
            elif item >= 0:
                ans.append('C')
            elif item >= -0.5:
                ans.append('D')
            elif item >= -1:
                ans.append('E')
            elif item <= -1:
                ans.append('F')

        return tuple(ans)
