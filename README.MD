<!-- ---------------------------------------------------------------------- -->
<h1>School election in Redis</h1>
<!-- ---------------------------------------------------------------------- -->
<hr>
This program simulates the election of various proposal in a school.<br/>
The program asks for name, surname and student id for login.<br/>
If the login is successfull the student can insert as many proposal as desired.
Every student can vote once for every proposal.<br/>

<hr>
After the login the student can:<br/>

<ul><li>n = New proposal</li>
    <li>v = Vote a proposal</li>
    <li>d = Proposal description</li></ul>

<h4>New proposal</h4>
The student can insert as many proposal as wished.<br/>

<h4>Vote a proposal</h4>
The student can vote for the proposal and see the proposal, the proposer, 
the description and the number of votes.<br/>

<h4>Proposal description</h4>
The student can see the proposal, the proposer, the description and the number
of vote.<br/>


<hr>
<h3>Database</h3>
<hr>
The Redis database is composed by 5 possible elements:<br/>

<ul>
    <li>
        <h3>student:<i>student_id</i>                </h3>
        <i>(string)</i>             <br/>   
        Contain name and username.  <br/><br/>
    </li>
    <li>
        <h3>proposer:proposal:<i>proposal_number</i> </h3>
        <i>(list)</i><br/>   
        Contain the student_id of the proposer.<br/><br/>
    </li>
    <li>
        <h3>proposal:<i>proposal_number</i>          </h3>
        <i>(hash)</i><br/>            
        Contain the proposal description, the 
        proposer and the number of votes.<br/><br/>
   </li>
   <li>
       <h3>elector:proposal:<i>proposal_number</i>   </h3>
       <i>(list)</i><br/>  
       Contain the student_id of the proposer<br/><br/>
   </li>
   <li>
       <h3>votes:proposal                            </h3>
       <i>(zset)</i><br/>                           
       Contain the list of the proposal.<br/><br/>
   </li></ul>

