from KBaseReport.KBaseReportClient import KBaseReport
from time import time
import os


def build_report(callback_url, scratch_dir, results, batch_size, workspace_id):
    """
    Expects a sets of batch results in the format given by the spec.
    That is, a dict, mapping each child job id to the result of that job provided by KBParallel.

    This uses those results to generate an HTML report, and returns a tuple of (report_name, report_ref)
    """
    report_client = KBaseReport(callback_url)
    timestamp = int(time() * 1000)
    report_name = "batch_report_{}".format(timestamp)
    report_dir = os.path.join(scratch_dir, report_name)
    os.makedirs(report_dir)

    html_info = write_html(report_dir, results, batch_size)
    report = report_client.create_extended_report({
        "html_links": [html_info],
        "direct_html_link_index": 0,
        "report_object_name": report_name,
        "workspace_id": int(workspace_id)
    })
    return (report['name'], report['ref'])


def write_html(report_dir, results, batch_size):
    html_file_name = "index.html"
    html_file_path = os.path.join(report_dir, html_file_name)

    """
    Something like:

    16 total jobs were submitted.
    0 cumulative failures (not counting retries)
    Approximate 2 hrs cumulative runtime

    job_id_1    final_state    module   method  version
    """
    total_line = "<div><b>{}</b> total jobs were submitted</div>".format(batch_size)
    num_fail = count_fails(results)
    fail_line = "<div><b>{}</b> jobs were unable to complete (not counting retries)</div>".format(num_fail)
    run_time = calc_run_time(results)
    runtime_line = "<div>Approximately {} cumulative runtime (walltime)</div>".format(run_time)

    header = "<div style='padding: 5px 0'>{}{}{}</div>".format(total_line, fail_line, runtime_line)

    job_rows = list()
    for job_id in sorted(results.keys()):
        res = results[job_id]
        fn = res.get('result_package', {}).get('function', {})
        module_name = fn.get('module_name', 'Unknown_module')
        app_name = fn.get('method_name', 'unknown_method')
        app_id = '.'.join([module_name, app_name])
        final_status = res.get('final_job_state', {}).get('job_state', 'unknown')
        app_version = fn.get('version', 'unknown')
        job_rows.append("<tr><td>{}</td></tr>".format("</td><td>".join([job_id, final_status, app_id, app_version])))

    table_header = "<tr><th>Job id</th><th>Final status</th><th>App id</th><th>Module version</th></tr>\n"
    job_table = "<table>{}{}</table>".format(table_header, "\n".join(job_rows))

    html_content = "<html>{}<br>{}</html>".format(header, job_table)

    with open(html_file_path, "w") as outfile:
        outfile.write(html_content)

    return {
        "path": report_dir,
        "name": "index.html",
        "description": "Batch Report"
    }


def calc_run_time(results):
    total_ms = 0
    for res in results.values():
        start_time = res.get('final_job_state', {}).get('exec_start_time', 0)
        end_time = res.get('final_job_state', {}).get('finish_time', 0)
        run_time = end_time - start_time
        if (run_time > 0):
            total_ms = total_ms + run_time
    s, ms = divmod(total_ms, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    time_str = ""
    if (d > 0):
        time_str = time_str + "{}d ".format(int(d))
    if (h > 0):
        time_str = time_str + "{}h ".format(int(h))
    if (m > 0):
        time_str = time_str + "{}m ".format(int(m))
    if (s > 0):
        time_str = time_str + "{}s".format(int(s))
    return time_str


def count_fails(results):
    count = 0
    for res in results.values():
        if results.get('is_error') is True:
            count = count + 1
    return count
