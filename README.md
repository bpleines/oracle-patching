<h1>Oracle Binary Database Patching</h1>
<body>
<br>

<h2><u>Overview:</u></h2>
<ul>
<li>This is an automation application to apply quarterly oracle security patches to database binaries on Solaris 10</li>
<li>This application patches both 11.2.0.4 and 12.1.0.2 binaries - there is conditional logic which chooses the appropriate tasks to run for each binary version yet many of the steps overlap</li>
<li>
This entire automation application boils down to 4 inputs:
<ol>
<li><b>oracle_binary_version</b> - the oracle binary version to be patched</li>
<li><b>opatch_latest_zip</b> - the opatch utility software to be installed in case an upgrade is needed</li>
<li><b>oneoff_latest_zip</b> - the quarterly security patch to be applied</li>
<li><b>patch_identifier</b> - the string used to check proper patch application to databases</li>
</ol>
</li>
<li>These inputs can be consumed by a Tower survey instead of group_vars in Ansible Core.</li>
</ul>

<h2><u>Dependency List:</u></h2>
<ul>
<li>Input opatch and one-off zips are present on the sql server in /home/oracle/Patching</li>
<li>Other required oracle scripts present on sql server in /home/oracle/Patching</li>
<li>ansible_python_interpreter points to a python distribution with python >= v2.6 and pexpect >= v3.3 installed for that distribution. This is by default /usr/bin/python in group_vars but can be overridden on the group/host level in inventory by setting the ansible_python_interpreter variable </li>
<li>Sudo configured correctly in ansible.cfg - currently sudo_exe = /usr/local/bin/sudo. This can be overridden on the group/host level in inventory by setting the ansible_sudo_exe variable</li>
<li>Path to bash is /bin/bash</li>
<li>All relevant Oracle listeners are started and running prior to content execution</li>
<li>$ORACLE_HOME/bin/sqlplus is the path to run the sqlplus command</li>
<li>Interactive Oracle scripts do not generate prompts beyond which are covered by current pexpect responses. This one would require some extra development</li>
<li>Any individual Oracle script does not take > 1 hour to complete (current timeout setting). This setting can be adjusted in /library/expect.py</li>
</ul>
<br>

<h2><u>Inventory:</u></h2>
Don't run this in parallel! There should be two inventory subgroups for any patching inventory
<ol>
<li><b>oracle_patching</b> - oracle server(s) to patch</li>
<li><b>tower_server</b> - necessary for email error reporting | Note: ansible_user must be set in inventory. This user must be able to sudo to the oracle user</li>
</ol>
<br>

<h2><u>Tags=Roles=Documentation:</u></h2>
<ol>
<li><b>prerequisite</b> - running tags=prerequisite with patch_oracle.yml is always safe. This checks basic Ansible software requirements and discloses what databases are targeted with the patch. This content lives in the Ansible prep role.
</li>
<li><b>prep</b> - tags=prerequisite,prep does some oracle patching related checks ensuring presence of required files as well as assessing the opatch utility version.
<li><b>patching</b> - tags=prequisite,prep,patching does the core patching process where listeners are brought down, databases are stopped, and binaries are patched. This should be used sparingly or not at all.
</li>
<li><b>post</b> - tags=prequisite,prep,patching,post is the same thing as running the playbook tagless. Post ensures that the binary-relevant databases reflect the newly applied patch.
</li>
</ol>
<b>Significance:</b> Running just the prerequisite tasks can be done ahead of patching. Running prerequisite and prep ahead of time should make you extremely confident that the patching will work and would give a database team time to remedy one-off patching conflicts. Beyond this you should just run the playbook tagless.
<br>
<br>

<h2><u>Error Handling:</u></h2>
There were 4 spots identified as high points of failure. These are wrapped in Ansible rescue blocks that send email notifications to {{ email_distribution_group }} based on a failure. High-failure of points include:
ol>
<li>The opatch utility upgrade failed (prep)</li>
<li>There is a flagged one-off patch conflict that will interfere with patching (prep)</li>
<li>The command 'opatch apply' failed (patching)</li>
<li>The applied patch didn't apply to one or all databases (post)</li>
</ol>
<b>Significance:</b> In all cases, the strategy here is to send an email to {{ email_distribution_group }} defined in group_vars. This is why if possible running the prerequisite and prep content ahead of time will mitigate most of what could go wrong. The job logs will provide more insight to the root problem.
<br>
<br>

<h2><u>Testing! A note to a future developer:</u></h2>
IMPORTANT! Deprecation warnings are carefully suppressed in ansible.cfg, but the SUDO_EXE setting used with the Solaris /usr/local/bin/sudo location will be deprecated in Ansible v2.8.
</body>
