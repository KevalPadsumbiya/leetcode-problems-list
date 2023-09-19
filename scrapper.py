import requests
import locale
import subprocess
import json
from datetime import datetime, timedelta


def generate_submission_modal(submission_id, code):
    modal_id = f"modal-{submission_id}"
    modal_content = f"""
        <div class="modal fade" id="{modal_id}" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Submission {submission_id} Code</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <pre><code>{code}</code></pre>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
    """
    return modal_content

# Set the headers and payload for the first API request
headers = {
    'authority': 'leetcode.com',
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/json',
    'cookie': '{your-cookie}',
    'origin': 'https://leetcode.com',
    'random-uuid': '{your-random-uuid}',
    'referer': 'https://leetcode.com/problemset/all/?page=1',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'x-csrftoken': '{your-csrftoken}',
}

payload = {
    "query": "\n    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\n  problemsetQuestionList: questionList(\n    categorySlug: $categorySlug\n    limit: $limit\n    skip: $skip\n    filters: $filters\n  ) {\n    total: totalNum\n    questions: data {\n      acRate\n      difficulty\n      isFavor\n      status\n      title\n      titleSlug\n    }\n  }\n}\n    ",
    "variables": {
        "categorySlug": "",
        "skip": 0,
        "limit": 2831,
        "filters": {}
    },
    "operationName": "problemsetQuestionList"
}

url = 'https://leetcode.com/graphql/'

response = requests.post(url, headers=headers, json=payload)
data = response.json()

# Extract and process the problem data
problems = data['data']['problemsetQuestionList']['questions']

# Write HTML table to abc.txt
with open("lc_problems.html", "w") as f:
    f.write("""<!DOCTYPE html>
<html>
<head>
    <style>
    </style>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/1.11.5/css/dataTables.bootstrap5.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
  <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.4/dist/jquery.slim.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js"></script>
            <style>
            .data {
            border-bottom: 1px solid black; border-right: 1px solid black;
            color:black;
            }
            .subs {
            border-top: 1px solid black;
            color:black;
            }
            * {
            font-size:15px;
            }
            </style>

</head>
<body>
    <br><center><h1>All LeetCode problems with likes and dislikes</h1></center><br><br>
    <div class="container">
        <table class="table table-bordered table-hover" id="example">
            <thead>
                <tr>
                    <th>Url</th>
                    <th>Status</th>
                    <th>AcRate</th>
                    <th>Difficulty</th>
                    <th>Likes</th>
                    <th>Dislikes</th>
                </tr>
            </thead>
            <tfoot>
                <tr>
                    <th>Url</th>
                    <th>Status</th>
                    <th>AcRate</th>
                    <th>Difficulty</th>
                    <th>Likes</th>
                    <th>Dislikes</th>
                </tr>
            </tfoot>
            <tbody>
    """)

    prob=1
    for problem in problems:
        titleSlug = problem['titleSlug']
        print(prob, titleSlug, problem['status'])
        prob+=1
        # Set the headers and payload for the second API request
        payload_question = {
            "query": "\n    query questionTitle($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    title\n    titleSlug\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n  }\n}\n    ",
            "variables": {
                "titleSlug": titleSlug
            },
            "operationName": "questionTitle"
        }

        response_question = requests.post(url, headers=headers, json=payload_question)
        data_question = response_question.json()

        question = data_question['data']['question']

        # Determine the row class based on status
        td_style = "background-color: #90EE90;" if problem['status'] == "ac" else ""

        formatted_likes = locale.format_string("%d", question['likes'], grouping=True)
        formatted_dislikes = locale.format_string("%d", question['dislikes'], grouping=True)

        # Set the headers and payload for the second API request (CURL)
        curl_command = [
            "curl",
            "--location",
            "https://leetcode.com/graphql/",
            "--header", "Content-Type: application/json",
            "--header", "Cookie: {your-cookie}",
            "--data", f'{{"query":"query questionContent($titleSlug: String!) {{ question(titleSlug: $titleSlug) {{ content }} }}" ,"variables": {{"titleSlug":"{titleSlug}"}} ,"operationName":"questionContent"}}'
        ]

        # Execute the CURL command and capture the output
        response = subprocess.check_output(curl_command, text=True)

        # Parse the JSON response
        data_question = json.loads(response)

        # Extract the 'content' attribute from the JSON response
        content = data_question['data']['question']['content']

        # Create a Bootstrap modal for each problem
        f.write(f"""
        <div class="modal fade" id="modal-{titleSlug}" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">{titleSlug} Content</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <!-- Place the 'content' attribute value here -->
                        {content}

                        <!-- Submissions table will be displayed here -->
                            <!-- Submissions table will be displayed here -->
                        <br><hr style="border: 1px solid black;">
                        <b>Submissions:</b><br><br>
                           <div class="subs row">
                            <div class="data col">Status</div>
                            <div class="data col" >Submission time (YYYY-MM-DD)</div>
                            <div class="data col" >Language</div>
                            <div class="data col" >Runtime</div>
                            <div class="data col" >Memory</div>
                            <div class="data col">Code</div>
                            </div>
        """)

         # Set the headers and payload for the third API request to fetch submissions (only for AC problems)
        if problem['status'] == 'ac':
            submissions_curl_command = [
                "curl",
                "--location",
                "https://leetcode.com/graphql/",
                "--header", "Cookie: {your-cookie}",
                "--header", "Content-Type: application/json",
                "--data", f'{{"query":"query submissionList($offset: Int!, $limit: Int!, $lastKey: String, $questionSlug: String!, $lang: Int, $status: Int) {{ questionSubmissionList(offset: $offset, limit: $limit, lastKey: $lastKey, questionSlug: $questionSlug, lang: $lang, status: $status) {{ lastKey hasNext submissions {{ id title titleSlug status statusDisplay lang langName runtime timestamp url isPending memory hasNotes notes flagType topicTags {{ id }} }} }} }}","variables": {{"questionSlug":"{titleSlug}","offset":0,"limit":20,"lastKey":null}},"operationName":"submissionList"}}'
            ]

            # Execute the CURL command to fetch submissions
            submissions_response = subprocess.check_output(submissions_curl_command, text=True)

            # Parse the JSON response for submissions
            submissions_data = json.loads(submissions_response)
            submissions = submissions_data['data']['questionSubmissionList']['submissions']

            # Populate the submissions table
            for submission in submissions:
                status_display = submission['statusDisplay']
                timestamp = int(submission['timestamp'])
                lang_name = submission['langName']
                runtime = submission['runtime']
                memory = submission['memory']
                submission_id = submission['id']

                if status_display != "Accepted":
                    continue

                # Convert Unix timestamp to IST
                ist_timestamp = datetime.utcfromtimestamp(timestamp) + timedelta(hours=5, minutes=30)

                # Format the IST timestamp as a string
                formatted_ist_timestamp = ist_timestamp.strftime('%Y-%m-%d')
                
                # Set the headers and payload for the first API request (CURL)
                curl_command = [
                    "curl",
                    "--location",
                    "https://leetcode.com/graphql/",
                    "--header", "Cookie: {your-cookie}",
                    "--header", "Content-Type: application/json",
                     "--data", f'{{"query": "query submissionDetails($submissionId: Int!) {{ submissionDetails(submissionId: $submissionId) {{ code timestamp statusCode }} }}", "variables": {{"submissionId": "{submission_id}"}} ,"operationName": "submissionDetails"}}'
                ]

                # Execute the CURL command and capture the output
                response = subprocess.check_output(curl_command, text=True)

                # Parse the JSON response
                data_submission = json.loads(response)

                # Extract and print the code
                code = data_submission['data']['submissionDetails']['code']
                # Generate the modal content for this submission
                submission_modal = generate_submission_modal(submission_id, code)

                modal_id = f"modal-{submission_id}"

                f.write(f"""
                    <div class="subs row">
                        <div class="data col" style="color:limegreen;">{status_display}</div>
                        <div class="data col" >{formatted_ist_timestamp}</div>
                        <div class="data col" >{lang_name}</div>
                        <div class="data col" >{runtime}</div>
                        <div class="data col" >{memory}</div>
                        <div class="data col"><a class="btn btn-primary" data-toggle="collapse" href="#collapseExample{submission_id}" role="button" aria-expanded="false" aria-controls="collapseExample">
    View Code
  </a></div>
  <div class="collapse" id="collapseExample{submission_id}">
  <div class="card card-body">
  <pre style="font-size:15px;">{code}</pre>
  </div>
</div>
                    </div>
                """)
                
                # Write the modal content to your HTML file
                f.write(submission_modal)

            f.write(f"""
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
            """)

        # Modify this line to include two links in one column
        f.write(f"<tr><td style=\"{td_style}\"><a href='https://leetcode.com/problems/{titleSlug}/' target='_blank'>{titleSlug}</a> | <a href='javascript:void(0);' data-toggle='modal' data-target='#modal-{titleSlug}'>View Description and Submissions</a></td><td style=\"{td_style}\">{problem['status']}</td><td style=\"{td_style}\">{problem['acRate']}</td><td style=\"{td_style}\">{problem['difficulty']}</td><td style=\"{td_style}\">{formatted_likes}</td><td style=\"{td_style}\">{formatted_dislikes}</td></tr>")


    f.write("""
            </tbody>
        </table>
    </div>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.11.5/js/dataTables.bootstrap5.min.js"></script>
    <script>
        $(document).ready(function() {
            $('#example').DataTable();
        });
    </script>
</body>
</html>
""")
