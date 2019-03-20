input_file = open('log_data.txt')


def get_tot_download_dict(input_log):
    ip_downloads = {}

    for line in input_log:
        line_list = line.split()
        date_list = line_list[1][1:-1].split(':')
        ip_downloads[date_list[0] + ' - ' + line_list[0]] = ip_downloads.get(date_list[0] + ' - ' + line_list[0],
                                                                             0) + int(line_list[2])

    input_log.seek(0)

    return ip_downloads


def get_hours_requests_dict(input_log):
    hours_downloads = {}

    for line in input_log:
        line_list = line.split()
        date_list = line_list[1][1:-1].split(':')
        hours_downloads[date_list[1]] = hours_downloads.get(date_list[1], 0) + 1

    input_log.seek(0)

    return hours_downloads


def find_top_downloader(date_ip_down):
    date_ip = dict()

    for key in date_ip_down:
        date = key.split()[0]
        ip = key.split()[2]
        downloaded = date_ip_down[key]
        if date in date_ip and downloaded < date_ip[date][1]:
            continue
        else:
            date_ip[date] = [ip, downloaded]

    return date_ip


def print_top_downloaders(top_downloaders):
    for date in top_downloaders:
        print(date, '-', top_downloaders[date][0])


def print_lazy_hour(hour_req):
    lazy_hour = None
    min_req = None
    for hour in hour_req:
        if min_req is None or hour_req[hour] < min_req:
            lazy_hour = hour
            min_req = hour_req[hour]

    print('The least busy hour is', lazy_hour, '\nIt had', min_req, 'requests only')


print_top_downloaders(find_top_downloader(get_tot_download_dict(input_file)))
print_lazy_hour(get_hours_requests_dict(input_file))
