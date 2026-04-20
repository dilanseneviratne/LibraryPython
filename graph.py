from plotly.graph_objs.layout.scene import xaxis, yaxis


def show_trend_graph(transactions):
    """
    Display a trend graph showing the number of books issued per date.
    Using pandas data processing and plotly for the interactive graph.
    """

    try:
        import pandas as pd
        import plotly.express as px
    except ImportError:
        print("\n Required Libraries not installed.")
        print(" Run: pip install numpy pandas plotly")
        input("\n Press Enter to return to menu...")
        return

    #Filter only issue transactions (type 1)
    issue_data = [
        {"data": tx.data, "count": 1}
        for tx in transactions
        if tx.tx_type == 1
    ]

    if not issue_data:
        print("\n No issue transactions found to plot.")
        input("\n Press Enter to return to menu...")
        return

    # Build dataframe and group by date
    df = pd.DataFrame(issue_data)
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
    df = df.groupby("date").sum().reset_index()
    df = df.sort_values("date")
    df["date_label"] = df["date"].dt.strftime("%d/%m/%Y")

    #Plot with plotly
    fig = px.bar(
        df,
        x = "date_label",
        y = "count",
        title = "Books Issued Per Date - Library Trend",
        labels = {"date_label": "Date", "count": "Books Issued"},
        color = "count",
        color_continuous_scale = "Blues",
        text = "count"
    )

    fig.update_layout(
        plot_bgcolor = "white",
        xaxis_title = "Date",
        yaxis_title = "Number of Books Issued",
        title_font_size = 20,
        xaxis_tickangle = -45,
        coloraxis_showscale = False
    )

    fig.update_traces(textposition = "outside")
    fig.show()

    print("\n Trend graph opened in your browser.")
    input("\n Press Enter to return to menu...")

