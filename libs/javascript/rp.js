// Ryan Burgert 2024
// A library for web development

const rp = {
	/**
	 * Constructs a URL by appending a query string, formed from a JSON object, to a base path.
	 * The function encodes both keys and values to ensure the URL is correctly formatted.
	 * This is particularly useful for constructing URLs with dynamic query parameters for HTTP requests,
	 * including handling nested JSON objects.
	 *
	 * @param {string} path - The base URL path to which the query string will be appended.
	 * @param {Object} queryJson - A JSON object containing the query parameters, including potential nested objects.
	 * @returns {string} A complete URL constructed from the base path and the encoded query parameters.
	 *
	 * @example
	 * // Example of building a URL with simple query parameters:
	 * const url = buildQueryUrl('https://example.com/api', { user: 'john', age: 30 });
	 * console.log(url);  // Outputs: "https://example.com/api?user=john&age=30"
	 *
	 * @example
	 * // Example of building a URL with a nested query object:
	 * const url = buildQueryUrl('https://example.com/api', {
	 *   user: 'jane',
	 *   details: { age: 29, city: 'New York' }
	 * });
	 * console.log(url);  // Outputs: "https://example.com/api?user=jane&details=%7B%22age%22%3A29%2C%22city%22%3A%22New%20York%22%7D"
	 *
	 * @example
	 * // Example of building a URL with a more complex nested structure:
	 * const url = buildQueryUrl('https://example.com/search', {
	 *   query: 'books',
	 *   filters: {
	 *     price: { min: 10, max: 50 },
	 *     availability: 'in stock',
	 *     tags: ['fiction', 'mystery']
	 *   }
	 * });
	 * console.log(url);  // Outputs: "https://example.com/search?query=books&filters=%7B%22price%22%3A%7B%22min%22%3A10%2C%22max%22%3A50%7D%2C%22availability%22%3A%22in%20stock%22%2C%22tags%22%3A%5B%22fiction%22%2C%22mystery%22%5D%7D"
	 */
	buildQueryUrl: function (path, queryJson) {
		const queryString = Object.entries(queryJson)
		.map(([key, value]) => {
			const encodedValue =
			typeof value === 'object'
				? encodeURIComponent(JSON.stringify(value))
				: encodeURIComponent(value);
			return `${encodeURIComponent(key)}=${encodedValue}`;
		})
		.join('&');
		return `${path}?${queryString}`;
	},
	webeval: {
		/**
		 * Evaluates the provided code using the webeval API.
		 * @param {string} code - The code to be evaluated.
		 * @param {Record<string, any>} [vars={}] - Additional variables to be passed to the evaluation context.
		 * @param {boolean} [sync=true] - Whether to execute the code synchronously or asynchronously.
		 * @returns {Promise<{ value: any, errored: boolean, error?: string }>} A promise that resolves to the evaluation result.
		 */
		evaluate: function (code, vars = {}, sync = true) {
		return fetch('/webeval/web/evaluate', {
			method: 'POST',
			headers: {
			'Content-Type': 'application/json',
			},
			body: JSON.stringify({
			code: code,
			vars: vars,
			sync: sync,
			content_type: 'application/json',
			}),
		}).then((response) => response.json());
		},
	},
};

// Make rp globally accessible
if (typeof window !== 'undefined') {
	window.rp = rp;
}
// Additionally, export it if in a module system
if (typeof module !== 'undefined' && typeof module.exports !== 'undefined') {
	module.exports = rp;
}