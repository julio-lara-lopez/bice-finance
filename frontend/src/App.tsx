import React, { useState, useEffect } from 'react';
import './App.css';

interface Expense {
  Fecha: string;
  Descripción: string;
  Monto: number;
  Categoria: string;
}

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string>('');
  const [expenses, setExpenses] = useState<Expense[]>([]);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage('Please select a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://localhost:8000/upload/', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setMessage(`File '${data.filename}' uploaded successfully.`);
        fetchExpenses(); // Refresh expenses after upload
      } else {
        setMessage('File upload failed.');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      setMessage('An error occurred while uploading the file.');
    }
  };

  const fetchExpenses = async () => {
    try {
      const response = await fetch('http://localhost:8000/expenses/');
      if (response.ok) {
        const data = await response.json();
        setExpenses(data);
      }
    } catch (error) {
      console.error('Error fetching expenses:', error);
    }
  };

  useEffect(() => {
    fetchExpenses();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Expense Management App</h1>
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload</button>
        <button onClick={fetchExpenses}>Refresh Expenses</button>
        {message && <p>{message}</p>}
      </header>
      <div className="expense-table">
        <h2>Expenses</h2>
        <table>
          <thead>
            <tr>
              <th>Fecha</th>
              <th>Descripción</th>
              <th>Monto</th>
              <th>Categoria</th>
            </tr>
          </thead>
          <tbody>
            {expenses.map((expense, index) => (
              <tr key={index}>
                <td>{expense.Fecha}</td>
                <td>{expense.Descripción}</td>
                <td>{expense.Monto}</td>
                <td>{expense.Categoria}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
