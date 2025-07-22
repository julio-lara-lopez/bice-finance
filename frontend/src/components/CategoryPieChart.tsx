import React, { useEffect, useState } from 'react';
import { PieChart, Pie, Cell, Legend, Tooltip, ResponsiveContainer } from 'recharts';

interface CategorySummary {
  category: string;
  amount: number;
  percentage: number;
}

const COLORS = [
  '#FFBB28', // Transporte
  '#FF8042', // Supermercado
  '#0088FE', // Arriendo
  '#00C49F', // Otros
  '#FF6384', // Extra 1
  '#36A2EB', // Extra 2
  '#FFCE56', // Extra 3
  '#8A2BE2', // Extra 4
];

interface CategoryPieChartProps {
  refreshKey: number;
}

const CategoryPieChart: React.FC<CategoryPieChartProps> = ({ refreshKey }) => {
  const [data, setData] = useState<CategorySummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch('http://localhost:8000/expenses/categories-summary');
        if (!response.ok) {
          throw new Error('Error fetching data');
        }
        const result = await response.json();
        setData(result);
      } catch (err: any) {
        setError(err.message || 'Unknown error');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [refreshKey]);

  if (loading) return <div>Loading pie chart...</div>;
  if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;
  if (!data.length) return <div>No data available for pie chart.</div>;

  return (
    <div style={{ width: '100%', maxWidth: 600, margin: '0 auto' }}>
      <h2 style={{ textAlign: 'center', marginBottom: 16 }}>Distribución de Gastos por Categoría</h2>
      <ResponsiveContainer width="100%" height={420}>
        <PieChart
          width={520}
          height={420}
          margin={{ top: 80, right: 40, left: 40, bottom: 40 }}
        >
          <Pie
            data={data}
            dataKey="amount"
            nameKey="category"
            cx="50%"
            cy="55%" // Move chart a bit down to avoid top clipping
            outerRadius={140} // Slightly larger for better label spacing
            labelLine={false}
            label={({ name, percent }) => `${name}: ${((percent ?? 0) * 100).toFixed(1)}%`}
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(value: any) => [`$${value}`, 'Monto']} />
          <Legend
            layout="vertical"
            align="right"
            verticalAlign="middle"
            formatter={(value) => {
              const item = data.find(d => d.category === value);
              return `${value}: ${item ? item.percentage.toFixed(1) : 0}%`;
            }}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default CategoryPieChart;