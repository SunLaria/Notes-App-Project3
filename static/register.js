const root = ReactDOM.createRoot(document.getElementById('root'));


function RegisterForm() {
    return (
        <div id="register-form-div">
            <form method='post' id="register-form">
                <input class="form-input" type="text" placeholder="Username" name="username" />
                <input class="form-input" type="password" placeholder="Password" name="password" />
                <button id="register-button" type="submit">Register</button>
            </form>
            <button id="back-button" onClick={()=>{location.href='/login'}} >Back</button>
        </div>
    )
}

function Main() {
    return (
        <>
        <RegisterForm />
        </>

    )
}

root.render(<Main/>)