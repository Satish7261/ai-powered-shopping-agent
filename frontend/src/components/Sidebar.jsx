import {
    Image,
    Search,
    Sparkles,
    Star,
    ShieldCheck,
} from "lucide-react";



const suggestions = [

    "Find organic honey under $20",

    "Show products with 4.5+ rating",

    "Find olive oil under $15",

    "Find healthy snacks",

];



function Sidebar({
    onImageClick,
    onSuggestion,
}) {

    return (

        <aside className="sidebar">


            {/* Sidebar heading */}

            <div className="sidebar-heading">

                <div className="sidebar-heading-icon">

                    <Sparkles
                        size={18}
                    />

                </div>


                <div>

                    <h2>
                        Shop smarter
                    </h2>

                    <p>
                        Let AI find it for you
                    </p>

                </div>

            </div>



            {/* Image search */}

            <button
                className="image-search-card"
                onClick={onImageClick}
            >

                <div className="image-search-icon">

                    <Image
                        size={25}
                    />

                </div>


                <h3>
                    Shop by Image
                </h3>


                <p>
                    Upload a product photo
                    and find similar products.
                </p>


                <span className="upload-label">
                    Upload product image
                </span>

            </button>



            {/* Suggestions */}

            <div className="sidebar-section">

                <div className="section-heading">

                    <Search
                        size={15}
                    />

                    <span>
                        Try asking
                    </span>

                </div>


                <div className="suggestions">

                    {suggestions.map(
                        (suggestion) => (

                            <button
                                key={suggestion}
                                onClick={() =>
                                    onSuggestion(
                                        suggestion
                                    )
                                }
                            >

                                {suggestion}

                            </button>

                        )
                    )}

                </div>

            </div>



            {/* Features */}

            <div className="sidebar-features">


                <div className="feature-item">

                    <div className="feature-icon">

                        <Star
                            size={15}
                        />

                    </div>


                    <div>

                        <strong>
                            Smart Ratings
                        </strong>

                        <span>
                            Compare customer reviews
                        </span>

                    </div>

                </div>



                <div className="feature-item">

                    <div className="feature-icon">

                        <ShieldCheck
                            size={15}
                        />

                    </div>


                    <div>

                        <strong>
                            Safe Checkout
                        </strong>

                        <span>
                            Orders require confirmation
                        </span>

                    </div>

                </div>


            </div>


        </aside>

    );

}


export default Sidebar;