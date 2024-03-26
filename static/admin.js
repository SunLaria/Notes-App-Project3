const root = ReactDOM.createRoot(document.getElementById('root'));


function Statistics(p) {
    const [users,setUsers] = React.useState(p.users)
    const [notes,setNotes] = React.useState([])
    React.useEffect(()=>{
        axios.get("/api/user?all=notes")
        .then((response)=>{setNotes(response.data)})
    },[])
    return(
        <div id="statistics">
            <div>Statistics</div>
            <div>Users: {users.length}</div>
            <div>Notes: {notes.length}</div>
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
            .then((response)=>{console.log(response.data.result);})
            document.getElementById(id).remove();
        }
    }
    const resetPasswordEvent = (id) =>{
        axios.patch("/api/user",{user_id:id,password:newPassword})
        .then((response)=>{console.log(response.data.result)});
        setEditMode(false)
    }
    return(
        <tr id={user.id} key={user.id}>
            <td>{user.id}</td>
            <td>{user.username}</td>
            <td>{user.created_at}</td>
            <td><button onClick={()=>{deleteEvent(user.id)}}>Delete</button></td>
            <td>
            {editMode?
            <>
                <input className="user-row-input" type="password" onChange={(e)=>{setNewPassword(e.target.value)}} />
                <button onClick={()=>{resetPasswordEvent(user.id)}}>v</button>
                <button onClick={()=>{setEditMode(false)}}>x</button>
            </>
                :<button onClick={()=>{setEditMode(true)}}>Reset Password</button>}
            </td>
        </tr>

    )
}


function UsersTable(p){
    const [users,setUsers] = React.useState(p.users)
    return(
        <div id="users-table-div">
        <table id="users-table">
            <tbody>
            <tr>
                <th>User ID</th>
                <th>Username</th>
                <th>Created At</th>
            </tr>
            {Array.from(users).map((user)=>{
                return <UserRow user={user}/>  })}
        </tbody>
        </table>
        </div>
    )
}


function AdminInterface(p){
    const [users,setUsers] = React.useState(p.users)

    return(
        <>
            <Statistics users={users} />
            <UsersTable users={users}/>
        </>
    )
}

function Main() {
    const [users,setUsers] = React.useState([])

    React.useEffect(()=>{
        axios.get("/api/user?all=users")
        .then((response)=>{setUsers(response.data)})
    },[])
    
    return(
        <>
        {users.length>0?<AdminInterface users={users}/>:""}
        </>
    )
}

root.render(<Main/>)