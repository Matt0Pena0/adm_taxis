export const formatCurrency = (value) => {
  if (value === undefined || value === null) return '$ 0,00';
  return new Intl.NumberFormat('es-UY', {
    style: 'currency',
    currency: 'UYU',
  }).format(value);
};

export const formatDate = (dateString) => {
  if (!dateString) return '-';
  const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
  return new Date(dateString + 'T00:00:00').toLocaleDateString('es-ES', options);
};