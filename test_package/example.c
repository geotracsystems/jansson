#include <stdio.h>
#include "jansson.h"

int main()
{
	char test_json[128] = "{ \"test\": 5 }\0";

	json_t *root;

	json_error_t error;

	root = json_loads(test_json, 0, &error);
	if(!root)
	{
		json_decref(root);
		return 1;
	}

	char *testBuffer = json_dumps(root, JSON_INDENT(2));
	printf("JSON Out: %s\n", testBuffer);
	free(testBuffer);

	json_decref(root);

	printf("SUCCESS\n");

	return 0;
}
