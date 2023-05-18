import React, { useState } from 'react';
import axios from 'axios';
import './test.css'; // import CSS file

function UserList() {
  const [users, setUsers] = useState([]);

  const fetchUsers = async (username, password) => {
    try {  
      console.log("hello")
      const response = await axios.get(`http://localhost:5002/login?username=${username}&password=${password}`);
      const response2 = await axios.get(`http://localhost:5002/all_users`);
      console.log(response)
      console.group(response2.data)
      setUsers(response2.data);
    } catch (error) {

      console.error(error);
    }
  };

  return (
    <div className="user-list-container">
      <h2>User List</h2>
      <button onClick={() => fetchUsers('Dina', 'Michelson')}>Fetch Users</button>
      <ul>
        {users.map((user) => (
          <li key={user.first_name}>{user.last_name}</li>
          
        ))}
      </ul>
    </div>
  );
}

export default UserList;
