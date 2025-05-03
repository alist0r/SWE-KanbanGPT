import { useState } from 'react';

const Task_Button = ({title, prvRank, prvCol}) => {
	const [rank, setRank] = useState(prvRank);
	const [col, setCol] = useState(prvCol);
	return (
		<div style={{backgroundColor: "red"}}>
		 <input 
		  value={rank} 
		  onChange={e => setRank(e.target.value)} 
		  type='number' 
		  size='1'>
		 </input>
		 <button>{title}</button>
		 <input
		  value={col}
		  onChange={e => setCol(e.target.value)} 
		  type='number'
		  size='1'>
		 </input>
		</div>
	)
}

export { Task_Button }
