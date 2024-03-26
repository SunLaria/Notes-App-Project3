const nav = ReactDOM.createRoot(document.getElementById('nav'));


function Nav(){
    return(
        <>
        <div id="site-name" onClick={()=>{location.replace("/")}}>Notes</div>
        <div>
        {document.getElementById("admin-check").innerText == "True"?
        <button onClick={()=>{location.replace('/admin')}}>Admin</button>:""    
        }
        {(location.href.split("/")[3]=="" || location.href.split("/")[3]=="admin")?
        <button onClick={()=>{location.replace('/logout')}}>Logout</button>:
        <button onClick={()=>{location.replace('/login')}}>Login</button>}
        </div>
        </>
    )
}


nav.render(<Nav/>)