import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    });
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary p-4 m-4 border border-red-500 rounded-lg bg-red-50">
          <h2 className="text-xl font-bold text-red-700 mb-2">Что-то пошло не так</h2>
          <details className="text-sm text-gray-700">
            <summary>Подробности ошибки</summary>
            <pre className="mt-2 p-2 bg-gray-100 rounded">
              {this.state.error && this.state.error.toString()}
            </pre>
          </details>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary; 