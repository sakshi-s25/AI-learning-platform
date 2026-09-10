const express = require('express')
const data = require("./mock_dataset_100.json")
const app = express();
const port = 9000;

const users = Array.isArray(data) ? data : (data.users || Object.values(data));
//Routes
app.get('/users',(req,res) => {
    const  html =`
    <ul>
        ${users.map(user => `<li>${user.name}</li>`).join(' ')}
    </ul>
    `;
    
    res.send(html);

})
app.get('/api/users',(req,res) => {
    return res.json(users);

});
app.get("/api/users/:id",(req,res) =>{
    const id = Number(req.params.id);
    const  user = users.find(user => user.id === id);
    return res.json(user);
});

app.listen(port,()=> console.log('Server started on port :',port))
