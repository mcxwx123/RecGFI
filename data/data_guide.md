Run the following scripts with Python to get data for the first time point (t=0) / second time point (t=1) of issues.
    
```shell
import json

with open('issuedata.json') as f:
    issuestr = json.load(f)
issuedic = json.loads(issuestr)
issuedata = issuedic['issuedata']
lst=[]
for i in range(len(issuedata)):
    lst.append(issuedata[i][t])
```

Attributes:
        issue_id, proid, owner_id, rpt_id, cls_id: Id of the issue, project, project owner, issue repoter, issue resolver on GHTorrent
        issuet: The time when the issue is created
        reft: The time when the issue is assigned or linked to a pull request
        clst: The time when the issue is closed
        language: Programming language of the project
        clscmt: Issue resolver's commits to this repo, before the issue is resolved
        usedt: The time used to solve the issue
        fromcmt: If the is closed with a commit
        isslist: id of issues in the project
        
        ---------- Content ----------

        title: Issue title
        body: Issue description
        body: Issue description
        labels: The number of different labels ([GFI-signal, Bug, Test, Build, Doc, Enhancement, Coding, New feature, Major, Medium, Untriaged, Triaged])

        ---------- Background ----------

        rptcmt: number of commits from issue reporter in the project
        rptallcmt: number of commits from issue reporter on Github
        rptiss: number of repoted issues from the reporter in the project
        rptalliss: number of repoted issues from the reporter on Github
        rptpr: number of pulls from the reporter in the project
        rptallpr: number of pulls from the reporter on Github
        rptpronum: number of projects owned by the reporter
        rptstar: number of stars of projects owned by the reporter
        rptfoll: number of followers of the reporter
        rpthaslabel: the reporter has added label to the issue
        rpthasevent: the reporter has conducted events in the issue
        rpthascomment: the reporter has commented in the issue
        rptissues: id of issues reported by the reporter
        rptisscmtlist: for the issues reported by the reporter in the project, 'rptissues' record the number of commits of the resolver in the project

        ownercmt: number of commits from the owner in the project
        ownerallcmt: number of commits from the owner on Github
        owneriss: number of repoted issues from the owner in the project
        owneralliss: number of repoted issues from the owner on Github
        ownerpr: number of pulls from the owner in the project
        ownerallpr: number of pulls from the owner on Github
        ownerpronum: number of projects owned by the owner
        ownerstar: number of stars of projects owned by the owner
        ownerfoll: number of followers of the owner
        ownerissues: id of issues reported by the owner
        
        pro_star: Number of stars
        proclspr: Number of closed pull requests
        procmt: Number of commits
        contributornum: Number of contributors
        crtclsissnum: Number of closed issues
        openiss: Number of open issues
        openissratio: Ratio of open issues over all issues
        clsisst: Median issue close time (in hours)

        ---------- Dynamics ----------
        events: contains data of users who conduct the following events: 'labeled', 'subscribed', 'referenced', 'mentioned', 'closed', 'assigned', 
               'milestoned', 'unlabeled', 'moved_columns_in_project', 'locked', 'added_to_project', 'demilestoned', 'removed_from_project', 'unassigned', 
               'renamed', 'reopened', 'head_ref_force_pushed', 'transferred', 'unsubscribed', 'merged', 'head_ref_deleted', 'comment_deleted', 'review_requested', 
               'connected', 'marked_as_duplicate' and any of all event types. Data of user: [userpronum,userstar,userallcmt,usercmt,userfoll,useralliss,useriss,userallpr,userpr,userissues]
        commentbody: All issue comments
        commentusers: Features for all involved commenters, similar with 'events'
