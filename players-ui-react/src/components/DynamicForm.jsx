import React, { useContext } from 'react';
import { MyContext } from './MyProvider';

const DynamicForm = () => {
  const { data, setData } = useContext(MyContext);
  const fields = [
    { name: 'playerId', type: 'text' },
    { name: 'birthYear', type: 'number' },
    { name: 'birthMonth', type: 'number' },
    { name: 'birthDay', type: 'number' },
    { name: 'birthCountry', type: 'text' },
    { name: 'birthState', type: 'text' },
    { name: 'birthCity', type: 'text' },
    { name: 'deathYear', type: 'number' },
    { name: 'deathMonth', type: 'number' },
    { name: 'deathDay', type: 'number' },
    { name: 'deathCountry', type: 'text' },
    { name: 'deathState', type: 'text' },
    { name: 'deathCity', type: 'text' },
    { name: 'nameFirst', type: 'text' },
    { name: 'nameLast', type: 'text' },
    { name: 'nameGiven', type: 'text' },
    { name: 'weight', type: 'number' },
    { name: 'height', type: 'number' },
    { name: 'bats', type: 'select', options: ['R', 'L', 'B'] },
    { name: 'throws', type: 'select', options: ['R', 'L'] },
    { name: 'debut', type: 'date' },
    { name: 'finalGame', type: 'date' },
    { name: 'retroID', type: 'text' },
    { name: 'bbrefID', type: 'text' },
  ];


  const handleChange = (fieldName, value, type) => {
    setData({
      ...data, 
      formData: {
        ...data.formData,
        [fieldName]: convertType(type, value)
      }
    });

  };

  const convertType =(type, value)=> {
    switch(type){
      case 'number':
        return Number(value);
      case 'date':
        return Date(value);
      default:
        return value;    
    }
  }

  return (
    <span>
      {fields.map((field) => (
        <div key={field.name}>
          <label htmlFor={field.name}>{field.name}:</label>
          {field.type === 'select' ? (
            <select
              id={field.name}
              onChange={(e) => handleChange(field.name, e.target.value, field.type)}
            >
              <option value="">Select</option>
              {field.options.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          ) : (
            <input
              id={field.name}
              type={field.type}
              onChange={(e) => handleChange(field.name, e.target.value, field.type)}
            />
          )}
        </div>
      ))}
    </span>
  );
};

export default DynamicForm;
