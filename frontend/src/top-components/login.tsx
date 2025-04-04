import axios from 'axios'

const post_login = () => {
	//todo make login request
}

const login = (swap_screen: Function) => {
	return () => {
		return (
			<>
			<form>
			 <label>Username: </label>
			 <input name="username" />
			 <br />
			 <label>Password: </label>
			 <input name="password" />
			 <br />
			 <button onClick={post_login}>
			  login
			 </button>
			</form>
			or
			<br />
			<button onClick={swap_screen}>
			 create user
			</button>
			</>
		)
	}
}

export { login }
