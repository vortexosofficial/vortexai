import sys
import os
import logging

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

sys.path.append("{}/../src/".format(dir_path))
print(sys.path)

root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
root.addHandler(handler)


from knowledge import (
    ObjectID,
    HashValue,
    EmailObjectBuilder,
    ObjectRelationStore,
    KnowledgeStore,
    EmailObject,
    ImageObject,
)
from aios_kernel import LocalSentenceTransformer_Image_ComputeNode, ComputeTask
import asyncio
import unittest


class TestVectorSTorage(unittest.IsolatedAsyncioTestCase):
    async def test_object(self):
        data = HashValue.hash_data("1233".encode("utf-8"))
        print(data.to_base58())
        print(data.to_base36())

        data2 = HashValue.from_base58(data.to_base58())
        self.assertEqual(data.to_base36(), data2.to_base36())

        data2 = HashValue.from_base36(data.to_base36())
        self.assertEqual(data.to_base58(), data2.to_base58())

        email_folder = "F:\\system\\Downloads\\8081ffdb80925f5bff9c6ab9c4756c7d"
        email_object = EmailObjectBuilder({}, email_folder).build()
        
        id = email_object.calculate_id()
        print(f"got email object: {id.to_base58()}")
        
        # test encode & decode
        ret = email_object.encode()
        obj = EmailObject.decode(ret)
        id2 = obj.calculate_id()
        print(f"got email object: {id2.to_base58()}")
        self.assertEqual(id.to_base58(), id2.to_base58())
        
        ret2 = obj.encode()
        self.assertEqual(ret, ret2)
        
        images = email_object.get_rich_text().get_images()
        image_keys = list(images.keys())
        print("got image list: ", image_keys)
        
        image_id = images[image_keys[1]]
        print(f"got image object: {image_keys[1]} {image_id.to_base58()}")
        
        node = LocalSentenceTransformer_Image_ComputeNode();
        ret = node.initial()
        self.assertEqual(ret, True)
        
        task = ComputeTask()
        task.set_image_embedding_params(image_id)
        ret = await node.execute_task(task)
        print(ret)
        '''
        buf = KnowledgeStore().get_object_store().get_object(image_id)
        image_obj= ImageObject.decode(buf)
        file_size = image_obj.get_file_size()
        print(f"got image object: {image_id.to_base58()}, size: {file_size}")
        
     
        image_data = KnowledgeStore().get_chunk_reader().read_chunk_list_to_single_bytes(image_obj.get_chunk_list())
        self.assertEqual(file_size, len(image_data))
        
        from PIL import Image
        import io
        image = Image.open(io.BytesIO(image_data))
        image.show()
        
        from sentence_transformers import SentenceTransformer
        #model = SentenceTransformer('clip-ViT-B-32-multilingual-v1')
        model = SentenceTransformer('clip-ViT-B-32')
        model.encode(image, convert_to_tensor=True)
        '''

    def test_relation(self):
        obj1 = ObjectID.hash_data("12345".encode("utf-8"))
        obj2 = ObjectID.hash_data("67890".encode("utf-8"))
        obj3 = ObjectID.hash_data("abcde".encode("utf-8"))
        obj4 = ObjectID.hash_data("fghij".encode("utf-8"))
        print(obj1.to_base58(), obj2.to_base58(), obj3.to_base58())
        relation_store = KnowledgeStore().get_relation_store()
        relation_store.add_relation(obj1, obj2)
        relation_store.add_relation(obj1, obj2)
        relation_store.add_relation(obj2, obj3)

        relation_store.add_relation(obj1, obj3)
        relation_store.add_relation(obj1, obj4)

        objs = relation_store.get_related_objects(obj2)
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0], obj3)

        objs = relation_store.get_related_root_objects(obj1)
        self.assertEqual(len(objs), 2)
        self.assertEqual(obj3 in objs, True)
        self.assertEqual(obj4 in objs, True)
        # self.assertCountEqual(objs, [obj3, obj4])


if __name__ == "__main__":
    unittest.main()
