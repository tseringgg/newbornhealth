export interface IEnvironment { 
    name: string;
    production?: boolean;
}

export const environment:IEnvironment = {
    name: 'development',
    production: false
}