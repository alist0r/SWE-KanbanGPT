import axios from 'axios'

const create_submission_handler = (url: string) => {
        return (formData) => {
          const json: any = {};
          // Placeholder values
          json["ColumnID"] = 1;
          formData.forEach((value, key) => {
                json[key] = value;
          });

          // Get token from localStorage
          const token = localStorage.getItem("access_token");
          console.log("Token being sent: ", token);

          axios.post(url, json, {
                headers: {
                  Authorization: `Bearer ${token}`,
                },
          })
          .then(function (response) {
                console.log(response);
          })
          .catch(function (error) {
                console.log(error);
          });
        };
  };



const Create_Board = () => {
	const submission_handler = create_submission_handler("http://localhost:8000/api/projects");
	return (
		<>
		 <form name="createProject" action={submission_handler}>
		 <label htmlFor="title">Title: </label>
		 <input name="title" id="title" /><br />
		 <label htmlFor="description">Description: </label>
		 <input name="description" id="description" /><br />
		 <button>create!</button>
		 </form>
		 or
		 <br />
		 <button>return to project select</button>
		</>
	)
}

export { Create_Board }
