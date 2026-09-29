#include "Angel.h"
#include <string>

const glm::vec3 WHITE(1.0, 1.0, 1.0);
const glm::vec3 BLACK(0.0, 0.0, 0.0);
const glm::vec3 RED(1.0, 0.0, 0.0);
const glm::vec3 GREEN(0.0, 1.0, 0.0);
const glm::vec3 BLUE(0.0, 0.0, 1.0);
const glm::vec3 YELLOW(1.0, 1.0, 0.0);
const glm::vec3 ORANGE(1.0, 0.65, 0.0);
const glm::vec3 PURPLE(0.8, 0.0, 0.8);

// 窗口变量
const int SQUARE_NUM = 6;
const int SQUARE_NUM_POINTS = 4 * SQUARE_NUM;
int Window;
int width = 600;		// 主窗口宽度
int height = 600;		// 主窗口高度
double offsetAngle = 0; // 角度偏移量
double delta = 0.01;	// 每次改变角度偏移的变化量
glm::vec3 WindowSquareColor = WHITE;

GLuint square_vao, program;

void framebuffer_size_callback(GLFWwindow *window, int width, int height)
{
	glViewport(0, 0, width, height);
}

// 获得正方形每个顶点的角度
double getSquareAngle(int point)
{
	return (M_PI / 4 + (M_PI / 2 * point)) + offsetAngle;
}

// 生成正方形上每个顶点的属性（位置和颜色）
void generateSquarePoints(glm::vec2 vertices[], glm::vec3 colors[], int squareNum, int startVertexIndex)
{
	double scale = 0.90;
	double scaleAdjust = scale / squareNum;
	glm::vec2 center(0.0, 0.0);
	int vertexIndex = startVertexIndex;
	for (int i = 0; i < squareNum; i++)
	{
		glm::vec3 currentColor = 0 == i % 2 ? WindowSquareColor : BLACK;
		for (int j = 0; j < 4; j++)
		{
			double currentAngle = getSquareAngle(j);
			vertices[vertexIndex] = glm::vec2(cos(currentAngle), sin(currentAngle)) * glm::vec2(scale, scale) + center;
			colors[vertexIndex] = currentColor;
			vertexIndex++;
		}
		scale -= scaleAdjust;
	}
}

void Init()
{
	glm::vec2 vertices[SQUARE_NUM * 4];
	glm::vec3 colors[SQUARE_NUM * 4];

	// 创建多个正方形
	generateSquarePoints(vertices, colors, SQUARE_NUM, 0);

	// 分配并绑定顶点数组对象
	glGenVertexArrays(1, &square_vao);
	glBindVertexArray(square_vao);

	// 创建并初始化顶点缓存对象。
	GLuint vbo;
	glGenBuffers(1, &vbo);
	glBindBuffer(GL_ARRAY_BUFFER, vbo);
	glBufferData(GL_ARRAY_BUFFER, sizeof(vertices) + sizeof(colors), NULL, GL_STATIC_DRAW);

	// 分别读取数据
	glBufferSubData(GL_ARRAY_BUFFER, 0, sizeof(vertices), vertices);
	glBufferSubData(GL_ARRAY_BUFFER, sizeof(vertices), sizeof(colors), colors);

	// 读取着色器并使用
	std::string vshader, fshader;

	vshader = "shaders/vshader.glsl";
	fshader = "shaders/fshader.glsl";

	// 创建着色器程序对象并使用。
	program = InitShader(vshader.c_str(), fshader.c_str());
	glUseProgram(program);

	// 从顶点着色器中初始化顶点的位置
	GLuint pLocation = glGetAttribLocation(program, "vPosition");
	glEnableVertexAttribArray(pLocation);
	glVertexAttribPointer(pLocation, 2, GL_FLOAT, GL_FALSE, 0, BUFFER_OFFSET(0));
	// 从顶点着色器中初始化顶点的颜色
	GLuint cLocation = glGetAttribLocation(program, "vColor");
	glEnableVertexAttribArray(cLocation);
	glVertexAttribPointer(cLocation, 3, GL_FLOAT, GL_FALSE, 0, BUFFER_OFFSET(sizeof(vertices)));

	// 黑色背景
	glClearColor(0.0, 0.0, 0.0, 1.0);
}

void Display()
{
	Init(); // 重绘时写入新的颜色数据
	glClear(GL_COLOR_BUFFER_BIT);

	glUseProgram(program);

	// 创建顶点数组对象
	glBindVertexArray(square_vao); // 绑定顶点数组对象

	for (int i = 0; i < SQUARE_NUM; i++)
	{
		glDrawArrays(GL_TRIANGLE_FAN, (i * 4), 4);
	}
}

void printHelp()
{
	printf("%s\n\n", "Interaction");
	printf("Keys to update the background color:\n");
	printf("'r' - red\n'b' - blue\n'w' - white\n");
	printf("Mouse click to update color:\n");
	printf("'left' - green\n'right' - yellow\n");
	printf("Mouse sroll to rotate:\n");
	printf("'up' - clockwise\n");
	printf("'down' - anticlockwise\n");
}

void mouse_button_callback(GLFWwindow *window, int button, int action, int mode)
{
	// @TODO: 课堂练习#1 - Step1  在窗口中添加鼠标点击，设置形状颜色
	if(button == GLFW_MOUSE_BUTTON_LEFT && action == GLFW_PRESS)
	{
		WindowSquareColor = GREEN;
	}
	else if(button == GLFW_MOUSE_BUTTON_RIGHT && action == GLFW_PRESS)
	{
		WindowSquareColor = YELLOW;
	}
}
void key_callback(GLFWwindow *window, int key, int scancode, int action, int mode)
{
	// @TODO: 课堂练习#1 - Step2  在窗口中添加键盘事件，更换形状颜色
	if(key == GLFW_KEY_R && action == GLFW_PRESS)
	{
		WindowSquareColor = RED;
	}
	else if(key == GLFW_KEY_B && action == GLFW_PRESS)
	{
		WindowSquareColor = BLUE;
	}
	else if(key == GLFW_KEY_W && action == GLFW_PRESS)
	{
		WindowSquareColor = WHITE;
	}
	else if(key == GLFW_KEY_O && action == GLFW_PRESS)
	{
		WindowSquareColor = ORANGE;
	}
	else if(key == GLFW_KEY_P && action == GLFW_PRESS)
	{
		WindowSquareColor = PURPLE;
	}
}
void sroll_callback(GLFWwindow *window, double xoffset, double yoffset)
{
	// @TODO: 课堂练习#2 控制正方形的旋转动画
	offsetAngle += yoffset * delta;
}

int main(int argc, char **argv)
{
	glfwInit();
	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
	glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

#ifdef __APPLE__
	glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
#endif

	// 创建窗口。
	GLFWwindow *window = glfwCreateWindow(width, height, "Interaction", NULL, NULL);
	glfwMakeContextCurrent(window);
	glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);
	// @TODO: 课堂练习#1 - Step1  将mouse_button_callback与window绑定
	glfwSetMouseButtonCallback(window, mouse_button_callback);
	// @TODO: 课堂练习#1 - Step2 将key_callback与window绑定
	glfwSetKeyCallback(window, key_callback);
	// @TODO: 课堂练习#2 将sroll_callback与window绑定
	glfwSetScrollCallback(window, sroll_callback);

	// 配置glad。
	if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
	{
		std::cout << "Failed to initialize GLAD" << std::endl;
		return -1;
	}
	Init();
	printHelp();
	// 循环渲染。
	while (!glfwWindowShouldClose(window))
	{
		Display();
		glfwSwapBuffers(window);
		glfwPollEvents();
	}
	glfwTerminate();
	return 0;
}
