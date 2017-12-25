def main():
    draw_pie_chart(rank=5,
                   year=2017,
                   return_type='png')

    # get_GDP(convert_krw=False,
    #           year=2017,
    #           rank=15,
    #           return_type='print')


def get_GDP(convert_krw=False,
            year=2017,
            rank=False,
            return_type='print'):
    import pandas as pd
    YEAR = int(year)
    RANK = rank
    # load GDP file
    df = pd.read_excel('data/imf-dm-export-20171222.xls')
    # rename the columns
    df = df[['GDP, current prices (Billions of U.S. dollars)', YEAR]]
    df.columns = ['Country', YEAR]
    # change string values of column YEAR to NaN
    df[YEAR] = pd.to_numeric(df[YEAR], errors='coerce')
    # remove collective subjects (ASEAN, Continents, et cetera)
    df = df.drop(df.index[194:])
    df = df.dropna().sort_values(by=YEAR, ascending=False)
    # truncate data if rank parameter is set
    if RANK:
        df = df.drop(df.index[int(RANK):])
    # add Rank column
    df = df.reset_index(drop=True)
    df.index += 1
    df.insert(loc=0, column='Rank', value=df.index)
    # if convert_krw is True, convert values into KRW
    if convert_krw:
        # KRW/USD (2017.10.01.): 1,145.90183373565
        # (currency rate refrence: https://ko.valutafx.com/KRW-USD.htm)
        # 1145.90183373565 * 1000000000 / 100000000 = 11459.0183373565
        df[YEAR] = df[YEAR] * 11459.0183373565
        df[YEAR] = df[YEAR].map('{:,.2f}'.format)
        df = df.rename(columns={YEAR: '{} (100 mil. of KRW)'.format(YEAR)})
    else:
        df = df.rename(columns={YEAR: '{} (1 bil. of USD)'.format(YEAR)})
    # if to_csv is True, export the data.
    if return_type == 'csv':
        file_name = '{}_GDP_data.csv'.format(YEAR)
        df.to_csv(file_name, sep=',', encoding='utf-8', index=False)
        print('[*] Successfully created [{}].'.format(file_name))
    elif return_type == 'df':
        return df
    elif return_type == 'print':
        print(df)


def draw_pie_chart(rank=5, year=2017, return_type='print'):
    import matplotlib.pyplot as plt
    # PARAMETERS
    RANK = int(rank)
    YEAR = int(year)
    TITLE_FONTSIZE = 40
    LABEL_FONTSIZE = 16
    LEGEND_FONTSIZE = 20
    LEGEND_BOX_POSITION = (1.0, 0.07)
    # get data using get_GDP function
    df = get_GDP(year=YEAR, return_type='df')
    # extract necessary data based on RANK parameter
    COLUMN_YEAR = '{} (1 bil. of USD)'.format(YEAR)
    total_num = df.index[-1]
    total_amount = df[COLUMN_YEAR].sum()
    df = df[:RANK]
    # convert countries and their amount into list()
    countries = df['Country'].tolist()
    amounts = df[COLUMN_YEAR].tolist()
    # append 'Others'
    countries += ['Others({} nations)'.format(total_num - RANK)]
    amounts += [total_amount - sum(amounts)]
    # set color maps
    colors = ['#640208', '#8F231D', '#B34737', '#D06F58', '#E29C81', '#E5CCB1']
    # create labels
    legend_labels = []
    chart_labels = []
    for i in range(len(countries)):
        ratio = '{:.2f}'.format(100 * amounts[i] / sum(amounts), countries[i])
        legend_labels.append('{}% {}'.format(ratio, countries[i]))
        chart_labels.append('{}\n({}%)'.format(countries[i], ratio))
    # draw pie chart
    fig1, ax1 = plt.subplots(figsize=(20, 10))
    patches, texts = ax1.pie(amounts,
                             labels=chart_labels,
                             colors=colors,
                             shadow=False, startangle=90)
    for text in texts:
        text.set_fontsize(LABEL_FONTSIZE)
    plt.legend(patches,
               legend_labels,
               bbox_to_anchor=LEGEND_BOX_POSITION,
               loc="lower right",
               fontsize=LEGEND_FONTSIZE,
               bbox_transform=plt.gcf().transFigure)
    ax1.axis('equal')
    ax1.set_title(
        '{} GDP Comparison Among TOP {} Nations\n'.format(YEAR, RANK),
        size=TITLE_FONTSIZE)

    # fig1.tight_layout()
    if return_type == 'print':
        plt.show()
    elif return_type == 'png':
        file_name = 'GDP_{}_TOP{}.png'.format(YEAR, RANK)
        plt.savefig(file_name)
        print('[*] Successfully created [{}].'.format(file_name))


if __name__ == "__main__":
    main()
