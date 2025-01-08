<!-- ---------------------------------------------------------------------- -->
<h1>School election in Redis</h1>
<!-- ---------------------------------------------------------------------- -->
<hr>
<p>
    This program simulates the election of various proposals in a school.<br />
    The program asks for name, surname, and student ID for login.<br />
    If the login is successful, the student can insert as many proposals as desired.
    Every student can vote once for every proposal.<br />
</p>
<hr>
<p>After the login, the student can:</p>
<ul>
    <li>n = New proposal</li>
    <li>v = Vote a proposal</li>
    <li>d = Proposal description</li>
</ul>

<h4>New proposal</h4>
<p>The student can insert as many proposals as wished.<br /></p>

<h4>Vote a proposal</h4>
<p>
    The student can vote for the proposal and see the proposal, the proposer,
    the description, and the number of votes.<br />
</p>

<h4>Proposal description</h4>
<p>
    The student can see the proposal, the proposer, the description, and the number
    of votes.<br />
</p>

<hr>
<h3>Database</h3>
<hr>
<p>The Redis database is composed of 5 possible elements:<br /></p>

<ul>
    <li>
        <h3>student:<i>student_id</i></h3>
        <p><i>(string)</i><br />
        Contains name and username.<br /><br /></p>
    </li>
    <li>
        <h3>proposer:proposal:<i>proposal_number</i></h3>
        <p><i>(list)</i><br />
        Contains the student_id of the proposer.<br /><br /></p>
    </li>
    <li>
        <h3>proposal:<i>proposal_number</i></h3>
        <p><i>(hash)</i><br />
        Contains the proposal description, the proposer, and the number of votes.<br /><br /></p>
    </li>
    <li>
        <h3>elector:proposal:<i>proposal_number</i></h3>
        <p><i>(list)</i><br />
        Contains the student_id of the proposer.<br /><br /></p>
    </li>
    <li>
        <h3>votes:proposal</h3>
        <p><i>(zset)</i><br />
        Contains the list of the proposals.<br /><br /></p>
    </li>
</ul>
