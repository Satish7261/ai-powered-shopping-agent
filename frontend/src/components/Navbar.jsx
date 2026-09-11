import {
    ShoppingBag,
    Sparkles,
    Circle,
} from "lucide-react";


function Navbar({ connected }) {

    return (

        <header className="navbar">


            {/* Logo */}

            <div className="brand">

                <div className="brand-logo">

                    <ShoppingBag
                        size={21}
                    />

                </div>


                <div className="brand-text">

                    <h1>
                        ShopAI
                    </h1>

                    <span>
                        Intelligent Shopping
                    </span>

                </div>

            </div>



            {/* Center text */}

            <div className="navbar-center">

                <Sparkles
                    size={15}
                />

                <span>
                    AI-powered shopping assistant
                </span>

            </div>



            {/* Connection status */}

            <div
                className={
                    `status-pill ${
                        connected
                            ? "status-online"
                            : "status-offline"
                    }`
                }
            >

                <Circle
                    size={8}
                    fill="currentColor"
                />

                <span>

                    {
                        connected
                            ? "AI Online"
                            : "Offline"
                    }

                </span>

            </div>


        </header>

    );

}


export default Navbar;