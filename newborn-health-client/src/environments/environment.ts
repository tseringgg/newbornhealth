export interface IEnvironment { 
    name: string;
    production?: boolean;
    apiUrl: string;
}

export const environment:IEnvironment = {
    name: 'development',
    apiUrl: 'http://localhost:4200',
    production: false
}