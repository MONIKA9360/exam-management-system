import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Breadcrumb.css';

const Breadcrumb = ({ items }) => {
  const navigate = useNavigate();

  return (
    <div className="breadcrumb">
      {items.map((item, index) => (
        <React.Fragment key={index}>
          {index > 0 && <span className="breadcrumb-separator">›</span>}
          {item.path ? (
            <span 
              className="breadcrumb-link" 
              onClick={() => navigate(item.path)}
            >
              {item.label}
            </span>
          ) : (
            <span className="breadcrumb-current">{item.label}</span>
          )}
        </React.Fragment>
      ))}
    </div>
  );
};

export default Breadcrumb;
