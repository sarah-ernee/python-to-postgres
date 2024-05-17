import datetime

num_rows = 5596

start_date = datetime.datetime(2023, 1, 1)

with open("./sql_v2/update_shift_report.sql", "w") as sql_file:
    for i in range(num_rows):
        current_date = start_date + datetime.timedelta(days=(i // 2))
        
        update_query = f"UPDATE shift_report SET created_at = '{current_date}' WHERE report_uid = (SELECT report_uid FROM (SELECT report_uid, ROW_NUMBER() OVER (ORDER BY created_at) AS rn FROM shift_report) AS subquery WHERE rn = {i+1});\n"
        sql_file.write(update_query)


"C:/Users/Sarah/Desktop/python-to-postgres/sql_v2/update_shift_report.sql"