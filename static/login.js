const root = ReactDOM.createRoot(document.getElementById('root'));


function LoginForm() {
    return (
        <div id="login-form-div">
            <form method='post' id="login-form">
                <input class="form-input" type="text" placeholder="Username" name="username" />
                <input class="form-input" type="password" placeholder="Password" name="password" />
                <button id="login-button" type="submit">Login</button>
            </form>
            <button id="register-button" onClick={()=>{location.href='/register'}} >Register</button>
        </div>
    )
}

function Main() {
    return (
        <>
        <LoginForm />
        </>

    )
}

root.render(<Main/>)