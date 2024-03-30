const root = ReactDOM.createRoot(document.getElementById('root'));


function Statistics(p) {
    const [notes,setNotes] = React.useState([])
    React.useEffect(()=>{
        axios.get("/api/user?all=notes")
        .then((response)=>{setNotes(response.data)})
        .catch((error) => {console.error('Error fetching all notes:', error)});
    },[p.users])
    return(
        <div>
            <div  id="statistics">
            <div>Statistics</div>
            <div>Users: {p.users.length}</div>
            <div>Notes: {notes.length}</div>
            </div>
        </div>
    )    
}


function UserRow(p){
    const [user,setUser] = React.useState(p.user) 
    const [editMode,setEditMode] = React.useState(false)
    const [newPassword,setNewPassword] = React.useState("")
    const deleteEvent = (id)=>{
        if (confirm('Are you sure you want to delete?')){
            axios.delete('/api/user',{params:{user_id:id}})
            .then((response)=>{
                console.log(response.data.result);
                p.setFunc(p.users.filter(user => user.id != id))
            })
            .catch((error) => {console.error('Error deleting user:', error)});
        }
    }
    const resetPasswordEvent = (id) =>{
        axios.patch("/api/user",{user_id:id,password:newPassword})
        .then((response)=>{
            console.log(response.data.result);
            setEditMode(false)
        })
        .catch((error) => {console.error('Error reset user password:', error)});
    }
    return(
        <tr id={user.id} key={user.id}>
            <td>{user.id}</td>
            <td>{user.username}</td>
            <td>{user.created_at}</td>
            <td>{user.admin==1?'True':'False'}</td>
            {user.username!="admin"?<td><button onClick={()=>{deleteEvent(user.id)}}>Delete</button></td>:""}
            <td>
            {editMode?
            <>
                <input className="user-row-input" type="password" onChange={(e)=>{setNewPassword(e.target.value)}} />
                <button className="choose-buttons" onClick={()=>{resetPasswordEvent(user.id)}}>✔️</button>
                <button className="choose-buttons" onClick={()=>{setEditMode(false)}}>❌</button>
            </>
                :<button onClick={()=>{setEditMode(true)}}>Reset Password</button>}
            </td>
        </tr>

    )
}


function UsersTable(p){
    return(
        <div id="users-table-div">
        <table id="users-table">
            <tbody>
            <tr>
                <th>User ID</th>
                <th>Username</th>
                <th>Created At</th>
                <th>Admin</th>
                <th></th>
                <th></th>

            </tr>
            {Array.from(p.users).map((user)=>{
                return <UserRow user={user} users={p.users} setFunc={p.setFunc}/> })}
        </tbody>
        </table>
        </div>
    )
}


function CreateButton(p){
    const [editMode,setEditMode] = React.useState(false)
    const [username, setUsername] = React.useState("")
    const [password, setPassword] = React.useState("")
    const [adminChecked, setAdminChecked] = React.useState(false);
    const createEvent = () => {
        console.log(adminChecked);
        axios.post("/api/user",{username:username,password:password,admin:adminChecked==true?"True":"False"})
        .then((response)=>{
            if (response.data.result.includes("User Created Successfully") == true){
                let newUserID = response.data.result.split('User Created Successfully, with id ')[1]
                let currentDate = new Date()
                p.setFunc([...p.users,{id:newUserID,username:username,admin:adminChecked?1:0,created_at:currentDate.toISOString().slice(0, 10)}])
                setEditMode(false)
            }
        })
        .catch((error) => {console.error('Error creating user:', error)});
    }
    return(
        <div id="create-button-div">
        <div>
        {editMode?
        <>
        <input className="user-row-input" type="text" placeholder="Username" onChange={(e)=>{setUsername(e.target.value)}}/>
        <input className="user-row-input" type="password" placeholder="Password" onChange={(e)=>{setPassword(e.target.value)}}/>
        <span style={{lineHeight:"2"}}>Admin:</span>
        <input id="admin-checkbox" type="checkbox" onChange={(e) => {setAdminChecked(e.target.checked)}} />
        <button className="choose-buttons" onClick={()=>{createEvent()}}>✔️</button>
        <button className="choose-buttons" onClick={()=>{setEditMode(false)}}>❌</button>
        </>
        :<button onClick={()=>{setEditMode(true)}}>Create</button>}
        </div>
        </div>
    )
}



function AdminInterface(p){
    return(
        <div id="admin-interface" >
            <Statistics users={p.users} />
            <UsersTable users={p.users} setFunc={p.setFunc} />
            <CreateButton users={p.users} setFunc={p.setFunc} />
        </div >
    )
}

function Main() {
    const [users,setUsers] = React.useState([])

    React.useEffect(()=>{
        axios.get("/api/user?all=users")
        .then((response)=>{
            setUsers(response.data);
        })
        .catch((error) => {console.error('Error fetching all users:', error)});
    },[])
    
    return(
        <>
        {users.length>0?<AdminInterface users={users} setFunc={setUsers} />:""}
        </>
    )
}

root.render(<Main/>)