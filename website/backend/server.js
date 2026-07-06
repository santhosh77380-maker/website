// ... existing code ...
import cors from 'cors';

const app = express();

// Middleware
app.use(cors()); // Intha line kandippa irukanum
app.use(express.json());

// ... rest of code ...