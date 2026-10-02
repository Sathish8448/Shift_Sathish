import React from 'react';

interface BadgeProps {
  count: number;
  absolute?: boolean;
}

const Badge: React.FC<BadgeProps> = ({ count, absolute = false }) => {
  if (count <= 0) return null;

  return (
    <span style={{
      ...styles.badge,
      ...(absolute ? styles.absolute : {})
    }}>
      {count > 99 ? '99+' : count}
    </span>
  );
};

const styles = {
  badge: {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#ef4444',
    color: 'white',
    fontSize: '0.65rem',
    fontWeight: 'bold',
    borderRadius: '9999px',
    minWidth: '1.25rem',
    height: '1.25rem',
    padding: '0 0.25rem',
    lineHeight: 1,
  },
  absolute: {
    position: 'absolute' as const,
    top: '-0.5rem',
    right: '-0.5rem',
  }
};

export default Badge;
