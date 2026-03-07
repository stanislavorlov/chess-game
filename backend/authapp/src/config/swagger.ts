import swaggerJsDoc, { Options } from 'swagger-jsdoc';
import swaggerUi from 'swagger-ui-express';
import path from 'path';
import { Application } from 'express';

const swaggerOptions: Options = {
    swaggerDefinition: {
        openapi: '3.0.0',
        info: {
            title: 'Auth API',
            version: '1.0.0',
            description: 'Authentication Service API',
        },
        servers: [
            {
                url: 'http://localhost:3000',
                description: 'Local server',
            },
        ],
        components: {
            securitySchemes: {
                bearerAuth: {
                    type: 'http',
                    scheme: 'bearer',
                    bearerFormat: 'JWT',
                },
            },
        },
    },
    apis: [path.join(__dirname, '../routes/*.routes.*')], // Adjust path since we are in src/config now
};

const swaggerDocs = swaggerJsDoc(swaggerOptions);

export const setupSwagger = (app: Application) => {
    app.use('/swagger', swaggerUi.serve, swaggerUi.setup(swaggerDocs));
};
