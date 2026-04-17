import billboard
import csv
from datetime import datetime, timedelta

def daterange(start_date, end_date):
    """Generate week dates"""
    current = start_date
    while current <= end_date:
        yield current
        current += timedelta(days=7)

def fetch_charts(chart_name, start_date_str, end_date_str, output_file):
    """Use billboard python package to get historic chart data"""
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "chart_date", "rank", "title", "artist",
            "weeks_on_chart", "peak_position", "last_position", "is_new"
        ])

        for date in daterange(start_date, end_date):
            date_str = date.strftime("%Y-%m-%d")
            print(f"Fetching {chart_name} for {date_str}...")

            try:
                chart = billboard.ChartData(chart_name, date=date_str)

                for entry in chart:
                    writer.writerow([
                        chart.date,
                        entry.rank,
                        entry.title,
                        entry.artist,
                        entry.weeks,
                        entry.peakPos,
                        entry.lastPos,
                        entry.isNew
                    ])

            except Exception as e:
                print(f"Failed for {date_str}: {e}")

if __name__ == "__main__":
    fetch_charts(
        chart_name="hot-100",
        start_date_str="2016-01-02", #first saturday of 2016
        end_date_str="2025-12-27", #last saturday of 2025 
        output_file="../data/hot100_history.csv"
    )