import unittest
from ArrayList import ArrayList
import random

class Test_ArrayList(unittest.TestCase):

    def generateLists(self, size, inputNone=False):
        arrayList = ArrayList(size)
        list = []
        for _ in range(size):
            item = None
            if not inputNone:
                item = random.randint(-1000,1000)
            arrayList.append(item)
            list.append(item)
        return arrayList, list

    def testContains(self):
        arrayList = self.generateLists(4)[0]
        arrayList.append(4)
        self.assertTrue(4 in arrayList, msg="item is not in the list")
        arrayList = self.generateLists(0)[0]
        self.assertFalse(4 in arrayList, msg="Item is in the list")

    def testGetItem(self):
        for i in range(7):
            arrayList, pyList = self.generateLists(i)
            for j in range(len(pyList)):
                self.assertEqual(arrayList[j], pyList[j], msg="item not equal")
                self.assertRaises(IndexError, arrayList.__getitem__,len(pyList))
                self.assertRaises(IndexError, arrayList.__getitem__, (-len(pyList)-1))
                self.assertEqual(arrayList[-(len(pyList)-j)], pyList[-(len(pyList)-j)], msg="index error")
    
    def testSetItem(self):
        for i in range(50):
            arrayList1 = self.generateLists(i, True)[0]
            arrayList2 = self.generateLists(i, True)[0]
            for j in range(i):
                negIndex = -(len(arrayList1)-j)
                item = random.randint(-1000,1000)
                arrayList1[j] = item
                arrayList2[negIndex] = item
                self.assertEqual(arrayList1[j], item, msg="item not equal")
                self.assertEqual(arrayList2[negIndex], item, msg="item not equal")
                self.assertEqual(arrayList1[j], arrayList2[negIndex], msg="item not equal")
            self.assertRaises(IndexError, arrayList1.__setitem__,len(arrayList1), 4)
            self.assertRaises(IndexError, arrayList2.__setitem__,-(len(arrayList2)+1), 5)

    def testEqual(self):
        for i in range(51):
            arrayList1, pyList = self.generateLists(i)
            self.assertEqual(arrayList1, pyList, msg="list not equal")
            pyList.append(5)
            self.assertNotEqual(arrayList1,pyList,msg="is equal")
        
        arrayList2 = ArrayList()
        arrayList2.append(5)
        arrayList2.append(6)
        self.assertNotEqual(arrayList2, (5,6), msg="is equal")
        list2 = [5,6,7]
        self.assertNotEqual(arrayList2,list2,msg="is equal")
        self.assertNotEqual(arrayList2, [5,7], msg="is equal")

    def testAppend(self):
        arrayList = self.generateLists(50)[0]
        arrayLen = len(arrayList.array)
        arrayList.append(2)
        self.assertEqual(2 * arrayLen, len(arrayList.array), msg="length of array double the size of original array")
    
    def testInsert(self):
        arraylist = self.generateLists(49)[0]
        self.assertIsNone(arraylist.insert(0,2), msg= print("insert success! length of the list is:",len(arraylist)))
        self.assertRaises(IndexError, arraylist.insert, 50, 2)
    
    def testRemove(self):
        arraylist = self.generateLists(3)[0]
        arraylist.append(5)
        self.assertIsNone(arraylist.remove(5), msg=print("item removed from the list, length after deletion: ", len(arraylist)))
        self.assertRaises(ValueError, arraylist.remove, 150)
    
    def testDelete(self):
        for i in range(1000):
            arrayList = self.generateLists(i)[0]
            for j in range(i):
                arrayList.delete(0)
                self.assertEqual(len(arrayList), i-(j+1))

        arraylist = self.generateLists(1)[0]
        self.assertIsNone(arraylist.delete(0), msg= print("length after deletion: ",len(arraylist)))
        self.assertRaises(IndexError, arraylist.delete, 0)

    def testSort(self):
        for i in range(51):
            arrayList, pyList = self.generateLists(i)
            for _ in range(i):
                self.assertEqual(arrayList.sort(), pyList.sort(), msg="sort ascending correct")
                self.assertEqual(arrayList.sort(reverse=True), pyList.sort(reverse=True), msg="sort descending correct")
            arrayList = ArrayList()
            self.assertIsNone(arrayList.sort(), msg="nothing to sort")

if __name__ == "__main__":
    unittest.main()