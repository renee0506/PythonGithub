import os.path as osp
import git
import maya.cmds as cmds
from maya import OpenMayaUI as omui
from PySide2 import QtWidgets
import shiboken2

#constructing classes
class UserInformation():
    remote_url = None
    repo = None

#-------------------------------------Back-End Functions----------------------------------------------------------------

#preparation
join = osp.join

#initialize
remote_path = None
repo = None

#initialize variable
LocalRepoField = None
LocalPathButton = None
remote_input = None

def LinkRemote():
    global remote_input
    UserInformation.remote_url = remote_input.text() 
    print 'Remote GitHub Repository URL: ' + UserInformation.remote_url
    
#Function: examine if user information exists
def userInformation(Repository):
    config_reader = repo.config_reader()
    
#Function: obtain text input, assign to remote path and print text input into History pane in script editior
#def LinkRemote( fieldID ):
    #global remote_path
    #remote_path = cmds.textField( fieldID, query=True, text=True)
    #print 'Remote GitHub Repository URL: ' + remote_path
    

#Function: LoadLocalDirectoryPath
def LoadLocalDirectoryPath():
    #create filebrowser
    singleFilter = "All Files (*.*)"
    local_repo = cmds.fileDialog2(fileFilter=singleFilter, dialogStyle=2, fm=3)[0]
    print 'Local Repository Location: ' +  local_repo
    #assign string input to local repo path variable
    global repo
    repo = Repo(path=local_repo)
 
    global LocalPathButton
    if cmds.button(CreateLocalButton, query=True, exists=True):
        #delete 'create local path' button if the button still exists, replace with textfield and regenerate the pick local path button
        cmds.deleteUI(CreateLocalButton, LocalPathButton)
        global LocalRepoField
        LocalRepoField = cmds.textField(parent='links', editable=False, tx=local_repo)
        LocalPathButton = cmds.button(parent='links', label='Local Directory Path', command='LoadLocalDirectoryPath()')
    #else:
        #replace the content in the textfield holding the local path
        #global LocalRepoField
        #cmds.deleteUI(LocalRepoField, LocalPathButton)
        #LocalRepoField = cmds.textField(parent='links', editable=False, tx=local_repo)
        #LocalPathButton = cmds.button(parent='links', label='Change Local Directory Path', command='LoadLocalDirectoryPath()')     

#Extract the name of the remote repository from the url
def FindRepoName(remotePathName, index):
    name = ''
    i = index
    found = False
    while found == False:
        if remotePathName[i] == '/':
            found = True
        else:
            name = remotePathName[i] + name
            i = i-1
    return name
    
#Function: CreateLocalRepo
def CreateLocalRepo():
    print '!!'
    #Extract the name of the remote repository from the url
    index = UserInformation.remote_url.find('.git')
    print UserInformation.remote_url
    name = FindRepoName(UserInformation.remote_url, index)
    print name
    #Open file browser to pick a directory to where the user wants to clone the remote repository
    singleFilter = "All Files (*.*)"
    local_repo = cmds.fileDialog2(fileFilter=singleFilter, dialogStyle=2, fm=3)[0] + '/' + name 
    UserInformation.repo = Repo.clone_from(UserInformation.remote_url, local_repo)
    #delete 'create local path' button, replace with textfield and regenerate the pick local path button
    #cmds.deleteUI(CreateLocalButton, LocalPathButton)
    #global LocalRepoField
    #global LocalPathButton
    #LocalRepoField = cmds.textField( editable=False, tx=local_repo)
    #LocalPathButton = cmds.button(label='Change Local Directory Path', command='LoadLocalDirectoryPath()')

#Function: Commit all
def CommitAll():
    repo.git.add('--all');
    print (repo.git)
    repo.index.commit('committed by Maya Git Integration')

#Function: Push    
def Push():
    local_branch = 'master'
    remote_branch = 'master'
    #push from local master to remote master
    remote = repo.remotes.origin.push(refspec='{}:{}'.format(local_branch, remote_branch))
        
#config_reader = repo.config_reader()
#config.set_value('user', 'email', 'meiqianye@gmail.com')
#config.set_value('user', 'name', 'Renee Mei')
print (repo)
#print config_reader.get_value("user", "email")

#-------User Interface-------------------------------------------------------------------------
       
window = QtWidgets.QWidget()
window.resize(500,200)
window.setWindowTitle('MayaGit')

windowLayout = QtWidgets.QGridLayout()  
windowLayout.setContentsMargins(50, 50, 50, 50)
windowLayout.setColumnStretch(1, -1)


remote_label = QtWidgets.QLabel('Remote Repository Url')
windowLayout.addWidget(remote_label, 0, 0)

remote_input = QtWidgets.QLineEdit()
windowLayout.addWidget(remote_input, 0, 1)
          
remote_button = QtWidgets.QPushButton("Link Remote Repository")
windowLayout.addWidget(remote_button, 0, 2)
remote_button.clicked.connect(LinkRemote)

local_label = QtWidgets.QLabel('Local Repository')
windowLayout.addWidget(local_label, 1, 0)

create_button = QtWidgets.QPushButton('Create Local Repository')
windowLayout.addWidget(create_button, 1, 1)
create_button.clicked.connect(CreateLocalRepo)

select_button = QtWidgets.QPushButton('Local Directory Path')
windowLayout.addWidget(select_button, 1, 2)

commitall_button = QtWidgets.QPushButton('Commit All')
windowLayout.addWidget(commitall_button, 2, 1)

push_button = QtWidgets.QPushButton('Push')
windowLayout.addWidget(push_button, 3, 1)
    
window.setLayout(windowLayout)
window.show()


    


#------------------Back-End Functions------------------------






#------------Start with User-Interface----------------------


#define id string for the window

winID = 'GitIntegrationUI'

#verify window existance
if cmds.window(winID, exists=True):
    cmds.deleteUI(winID)
    
#create fresh UI window
cmds.window(winID, title='GitHub Integration', widthHeight=[800, 500] )

cmds.frameLayout('master')
#Add 1st column
cmds.rowColumnLayout('links', numberOfColumns=3, columnAttach = [(1,'right',10), (3,'left', 10)], columnWidth=[(1, 250), (2, 250), (3,250)], rowSpacing =(10,10))

#Link remote
cmds.text(label='Remote Repository URL')
RemoteURL = cmds.textField()
cmds.button(label='Link', command='LinkRemote(RemoteURL)' )

#Link local
cmds.text(label='Local Repository')
CreateLocalButton = cmds.button('CreateLocalBtn', label='Create Local Repo', command='CreateLocalRepo()' )
LocalPathButton =cmds.button('LocalDirectoryBtn', label='Local Directory Path', command='LoadLocalDirectoryPath()')

cmds.setParent('master')
#Add 2nd column
cmds.rowColumnLayout(numberOfColumns=3, columnAttach = [(1,'right',10), (3,'left', 10)], columnWidth=[(1, 250), (2, 250), (3,250)], rowSpacing =(10,10))
#Add commit button
CreateCommitButton = cmds.button(label='Commit All', command='CommitAll()')
#Add push button
CreatePushButton = cmds.button(label='Push', command='Push()')

cmds.showWindow()
