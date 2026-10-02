import React from 'react';

interface ErrorMessageProps {
  title?: string;
  message: string;
  onRetry?: () => void;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ title = 'Error', message, onRetry }) => {
  return (
    <div style={styles.container}>
      <div style={styles.icon}>⚠️</div>
      <h3 style={styles.title}>{title}</h3>
      <p style={styles.message}>{message}</p>
      {onRetry && (
        <button style={styles.button} onClick={onRetry}>
          Try Again
        </button>
      )}
    </div>
  );
};

const styles = {
  container: {
    padding: '1.5rem',
    backgroundColor: '#fef2f2',
    border: '1px solid #f87171',
    borderRadius: '0.5rem',
    display: 'flex',
    flexDirection: 'column' as const,
    alignItems: 'center',
    textAlign: 'center' as const,
    margin: '1rem 0',
  },
  icon: {
    fontSize: '2rem',
    marginBottom: '0.5rem',
  },
  title: {
    color: '#991b1b',
    margin: '0 0 0.5rem 0',
    fontSize: '1.125rem',
    fontWeight: 'bold',
  },
  message: {
    color: '#b91c1c',
    margin: '0 0 1rem 0',
  },
  button: {
    padding: '0.5rem 1rem',
    backgroundColor: '#dc2626',
    color: 'white',
    border: 'none',
    borderRadius: '0.25rem',
    cursor: 'pointer',
    fontWeight: 'bold',
    transition: 'background-color 0.2s',
  }
};

export default ErrorMessage;
