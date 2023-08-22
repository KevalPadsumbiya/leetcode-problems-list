import requests
import locale

# Set the headers and payload for the first API request
headers = {
    # Your headers here
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
with open("/Users/kpadsumbiya/OneDrive - Chegg Inc/lc_problems.html", "w") as f:
    f.write("""<!DOCTYPE html>
<html>
<head>
    <style>
        /* Your styles here */
    </style>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/1.11.5/css/dataTables.bootstrap5.min.css" rel="stylesheet">
</head>
<body>
            <br><h1> All LeetCode problems with likes and dislikes</h1><br><br>
    <div class="container">
        <table class="table table-bordered table-hover table-striped" id="example">
            <thead>
                <tr>
                    <th>Url</th>
                    <th>AcRate</th>
                    <th>Difficulty</th>
                    <th>Likes</th>
                    <th>Dislikes</th>
                </tr>
            </thead>
            <tfoot>
                <tr>
                    <th>Url</th>
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
        print(prob,titleSlug)
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
        row_class = "ac" if problem['status'] == "ac" else ""

        formatted_likes = locale.format_string("%d", question['likes'], grouping=True)
        formatted_dislikes = locale.format_string("%d", question['dislikes'], grouping=True)
        f.write(f"<tr class='{row_class}'><td><a href='https://leetcode.com/problems/{titleSlug}/' target='_blank'>{titleSlug}</a></td><td>{problem['acRate']}</td><td>{problem['difficulty']}</td><td>{formatted_likes}</td><td>{formatted_dislikes}</td></tr>")

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
