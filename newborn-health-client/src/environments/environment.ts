export interface IEnvironment { 
    // name: string;
    production?: boolean;
    apiUrl: string;
}

export const environment:IEnvironment = {
    // name: 'development',
    // apiUrl: 'http://localhost:4200',
    apiUrl: 'http://127.0.0.1:5000/ask',
    production: false
}