#include <iostream>
#include <cstring>
#include <vector>
#include <queue>
#include <set>
#include <sstream>
#include <cmath>
#include <chrono>
using namespace std;
using namespace std::chrono;

const int N = 9;
const int targetSta[N] = {1, 2, 3, 8, 0, 4, 7, 6, 5};
const int targetPos[N] = {4, 0, 1, 2, 5, 8, 7, 6, 3};
// const int N = 16;
// // 所有元素的数量
// const int targetSta[N] = {1, 2, 3, 4,
//                           12, 13, 14, 5,
//                           11, 0, 15, 6,
//                           10, 9, 8, 7};
// // 目标状态
// const int targetPos[N] = {9, 0, 1, 2,
//                           3, 7, 11, 15,
//                           14, 13, 12, 8,
//                           4, 5, 6, 10};
//pos[i] 数字i 的下标应该为 什么 such 0 index is 9
const int dim = sqrt(N);
//dim 边长
const int LEFT = 1, RIGHT = 2, UP = 3, DOWN = 4;
//定义方向
struct Node
{
    int *status;
    Node *father;
    int weight, deepNum;
    // weight 为 h deepNum 为 g
};
// 节点 内容 1 状态 2 父节点指针 3 权重 4 已经遍历的深度
typedef pair<int, Node *> PII;
// pair 权重 结点指针
// 

int creaNum, closeNum;
// open 表中数量， close 表中数量
queue<Node *> closeQueue;
// close 表队列
set<string> vis;
// 集合vis string
priority_queue<PII, vector<PII>, greater<>> openQueue;
// 优先队列 open表
Node *getStart();
// 获取开始状态
bool checkVised(const int *test);
// 检查这个状态有没有被遍历过，如果有返回返回TRUE else add set return false
Node *A_star();
bool isSolve(int *start);
Node *move(Node *father, int dis);
// 父节点 目的地？？
int getZeroPos(const int *arr);
bool isEqual(const int *test1, const int *test2);
string toStr(const int *arr);
void deleteNode(Node *node);
void delAllNode();
void printAns(Node *state);
int heuFun(Node *newSta);
// 返回路径深度

int main()
{
    Node *initState = getStart();
    creaNum++, openQueue.push({initState->weight, initState});
    checkVised(initState->status);

    /* Time Test */
    auto start = high_resolution_clock::now();
    /*      A_star Function      */
    Node *endState = A_star();
    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<milliseconds>(stop - start);
    cout << "Time taken by function: "
         << duration.count() << " milliseconds" << endl;

    if (endState == NULL)
    {
        puts("No Solution!");
    }
    else
    {
        printf("Number of extension nodes: %d\n", closeNum);
        printf("Number of generated nodes: %d\n", creaNum);
        printAns(endState);
    }

    delAllNode();
    system("pause");
    return 0;
}

/**
 * Get the Initial state
*/
Node *getStart()
{
    Node *initState = new Node;
    initState->status = new int[N];
    // 建立所有元素的一维数组
    cout << "Please enter the initial state: \n";
    for (int i = 0; i < N; i++)
        cin >> initState->status[i];
    //输入一维数组
    initState->deepNum = 0;
    initState->father = NULL;
    initState->weight = heuFun(initState);
    return initState;
}

/**
 * If the state has visted, return true,
 * otherwise, return false and mark the state
 * @param test
 * @return true or fasle
*/
bool checkVised(const int *test)
{
    string s = toStr(test);
    // statue to string
    if (vis.find(s) != vis.end())
        return true;
    vis.insert(s);
    return false;
}

/**
 * A_star algorithm to solve the problem
*/
Node *A_star()
{
    // The initial state and the target state cannot reach each other
    if (!isSolve(openQueue.top().second->status))
        return NULL;

    // loop while open table is not empty
    while (!openQueue.empty())
    {
        Node *father = openQueue.top().second;
        //get f minest to father for explain child nodes
        closeNum++;
        // Move elements from the open table to the close table
        openQueue.pop();
        closeQueue.push(father);

        // Four directions of movement
        for (int i = 1; i <= 4; i++)
        {
            Node *newSta = move(father, i);
            if (newSta == NULL) continue;
            // can not 
            openQueue.push({newSta->weight, newSta});
            creaNum++;

            if (isEqual(newSta->status, targetSta))
            {
                // Find the target state
                return newSta;
            }
        }
    }
    return NULL;
}

/**
 * Determine whether the problem can be solved
 * @param start
 * @param targetSta
*/
bool isSolve(int *start)
{
    int startInver, targetInver;
    // 除零以外的逆序数
    for (int i = 0; i < N; i++)
    {
        for (int j = i + 1; j < N; j++)
        {
            // 跳过0 because  if start[j] == 0 跳过
            if (start[i] && start[j] && start[i] > start[j])
                startInver++;
            if (targetSta[i] && targetSta[j] && targetSta[i] > targetSta[j])
                targetInver++;
        }
    }

    if ((N - 1) % 2 == 0)
    {
        // if dim is odd 空格上下移动不影响整体逆序对的奇偶性
        return startInver % 2 == targetInver % 2;
    }
    else
    {
        int startZero = getZeroPos(start) / dim;
        int targetZero = getZeroPos(targetSta) / dim;
        int k = abs(startZero - targetZero);
        // 0的差值
        if (startInver % 2 == targetInver % 2)
        {
            // 相当于0 上下移动的次数
            // if inver num 相同 如果上下移动偶数次，可解
            return k % 2 == 0;
        }
        else
        {
            // if inver num 不同 if up or down odd times can solve
            return k % 2;
        }
    }
}

/**
 * Move the blank block to the given direction
 * @param father Status to be moved
 * @param dis Moving direction
 * @return If the movement is legal, return to the state after the movement, 
 *         otherwise return a null pointer
*/
Node *move(Node *father, int dis)
{
    int zeroPos = getZeroPos(father->status), newPos;
    // define newPos 
    // Initialize the new state
    Node *newSta = new Node;
    newSta->father = father;
    newSta->deepNum = father->deepNum + 1;
    newSta->status = new int[N];
    memcpy(newSta->status, father->status, sizeof(int) * N);

    // Determine the index of the grid to be swapped,
    // and check whether the swap is legal
    switch (dis)
    {
    case LEFT:
        newPos = zeroPos - 1;
        // turn left pos -1
        if (newPos < 0 || zeroPos % dim == 0)
        {
            // if origin is leftest => illegal
            delete (newSta);
            return NULL;
        }
        break;
    case RIGHT:
        newPos = zeroPos + 1;
        if (newPos >= N || newPos % dim == 0)
        {
            // if newpos is next line leftest => illegal
            // origin is rightest
            delete (newSta);
            return NULL;
        }
        break;
    case UP:
        newPos = zeroPos - dim;
        if (newPos < 0)
        {
            delete (newSta);
            return NULL;
        }
        break;
    case DOWN:
        newPos = zeroPos + dim;
        if (newPos >= N)
        {
            delete (newSta);
            return NULL;
        }
        break;
    default:
        break;
    }
    // legal
    // Swap two grid
    swap(newSta->status[zeroPos], newSta->status[newPos]);
    // Check if the status has been expanded
    if (checkVised(newSta->status))
    {
        deleteNode(newSta);
        return NULL;
    }
    newSta->weight = heuFun(newSta); // Obtain the heuristic function value
    return newSta;
}

/**
 * Find the position of the blank space
 * @param arr
 * @return
*/
int getZeroPos(const int *arr)
{
    //arr is statue
    for (int i = 0; i < N; i++)
    {
        if (arr[i] == 0)
            return i;
    }
    return -1;
}

/**
 * Return True if the two states are the same
 * @param test1
 * @param test2
 * @return true or false
*/
bool isEqual(const int *test1, const int *test2)
{
    return memcmp(test1, test2, sizeof(int) * N) == 0;
}

/**
 * Convert an array of integers to a string
 * @param arr
 * @return A string
*/
string toStr(const int *arr)
{
    stringstream ss;
    // 相当于sprintf 把数据输入到输入流
    for (int i = 0; i < N; i++)
        ss << arr[i] << ',';
        // 拼接所有元素，每个元素后面加，
    return ss.str();
    // 转成string
}

/**
 * Release the space pointed by the pointer
 * @param node 
*/
void deleteNode(Node *node)
{
    delete (node->status);
    delete (node);
    node = NULL;
}

/**
 * Backtracking output the movement process
 * @param state
*/
void printAns(Node *state)
{
    if (state == NULL)
        return;
    printAns(state->father);

    printf("The %d step: \n", state->deepNum);
    for (int i = 0; i < dim; i++)
    {
        for (int j = 0; j < dim; j++)
        {
            printf("%3d ", state->status[i * dim + j]);
        }
        puts("");
    }
}

/**
 * Delete all node
*/
void delAllNode()
{
    while (!openQueue.empty())
    {
        deleteNode(openQueue.top().second);
        openQueue.pop();
    }

    while (!closeQueue.empty())
    {
        deleteNode(closeQueue.front());
        closeQueue.pop();
    }
}

/**
 * Heuristic function 1: 
 * The sum of the number of grid that are not at the target position and the path depth 
 * @param newSta 
*/
// int heuFun(Node *newSta)
// {
//     int weight = newSta->deepNum;
//     for (int i = 0; i < N; i++)
//         weight += newSta->status[i] != targetSta[i];
//     return weight;
// }

/**
 * Heuristic function 2:
 * The sum of the distance between all grid and their target positions and the path depth
 * @param newSta
*/
// int heuFun(Node *newSta)
// {
//     int weight = newSta->deepNum;
//     for (int i = 0; i < N; i++)
//     {
//         int num = newSta->status[i];
//         int expePos = targetPos[num];
//         weight += abs(i / dim - expePos / dim) + abs(i % dim - expePos % dim);
//     }
//     return weight;
// }

/**
 * Heuristic function 3: The path depth
 * @param newSta
*/
int heuFun(Node *newSta)
{
    return newSta->deepNum;
}

/*
Test Data 1:
6 8 0
5 2 3
1 4 7
*/

/*
Test Data 2:
2 8 3
1 6 4
7 0 5
*/

/*
Test Data 3:
1 2 3
0 8 4？
6 7 5
*/

/*
Test Data 4:
1 2 3 4
11 13 5 6
10 12 0 8
9 14 15 7
*/