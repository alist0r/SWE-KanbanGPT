import axios from 'axios'

const post_login = () => {
	//todo make login request
}

//temporary function names just to get things working, i know swap_screen2 is bad
const login = (swap_screen: Function, swap_screen2: Function) => {
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
			<button onClick={swap_screen2}>
			 create task
			</button>
			</>
		)
	}
}

export { login }
